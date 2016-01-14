<?php
/**
 * Script configuration.
 */

$conf = Array(
    // The socket type can be 'unix' for connecting with the unix socket or 'tcp'
    // to connect to a tcp socket.
    'socketType'       => 'unix',
    // When using a unix socket the path to the socket needs to be set
    'socketPath'       => '/var/log/nagios/live',
    // When using a tcp socket the address and port needs to be set
    'socketAddress'    => '',
    'socketPort'       => '',
    // Modify the default allowed query type match regex
    'queryTypes'       => '(GET|LOGROTATE|COMMAND)',
    // Modify the matchig regex for the allowed tables
    'queryTables'      => '([a-z]+)',
);

class LiveException extends Exception {}


$LIVE = null;


/**
 * FUNCTIONS
 */

function livestatusCom() {
    global $conf;

    try {
        verifyConfig();

        // Run preflight checks
        if($conf['socketType'] == 'unix') {
            checkSocketExists();
        }

        checkSocketSupport();

        connectSocket();

        // Get the query (nope)
        //$query = getQuery();

        // number of services in each state (0 = OK, 1 = Warning, 2 = Critical, 3 = Unknown)
        // we filter the services acknowledged or for wich the host is acknowledged (feature request #001 et #002)
        $query = "GET services\nFilter: host_acknowledged = 0\nFilter: acknowledged = 0\nFilter: host_checks_enabled = 1\nStats: state = 0\nStats: state = 1\nStats: state = 2\nStats: state = 3\n";
        // number of host UP, total number of hosts (feature request #004)
        //$query2 = "GET hosts\nStats: state = 0\nStats: state != 9999\n";

        // Handle the query now
        // Output format is an array of an array (yeah!)
        $tab =  queryLivestatus($query);

	$resp = $tab[0];
        // first row of the first request: number of services OK
	$ok = $resp[0];
        // first row of the first request: number of services warning
	$warn = $resp[1];
        // first row of the first request: number of services critical
	$crit = $resp[2];
        // first row of the first request: number of services unknown
        $unkn = $resp[3];

	echo "{\"services\":{\"ok\":$ok, \"warn\":$warn, \"crit\":$crit, \"unknown\":$unkn}}";




        closeSocket();
        exit(0);
    } catch(LiveException $e) {
        echo 'ERROR: '.$e->getMessage();
        closeSocket();
        exit(1);
    }
}


function verifyConfig() {
    global $conf;

    if($conf['socketType'] != 'tcp' && $conf['socketType'] != 'unix')
        throw new LiveException('Socket Type is invalid. Need to be "unix" or "tcp".');

    if($conf['socketType'] == 'unix') {
        if($conf['socketPath'] == '')
            throw new LiveException('The option socketPath is empty.');
    } elseif($conf['socketType'] == 'tcp') {
        if($conf['socketAddress'] == '')
            throw new LiveException('The option socketAddress is empty.');
        if($conf['socketPort'] == '')
            throw new LiveException('The option socketPort is empty.');
    }
}

function closeSocket() {
    global $LIVE;
    @socket_close($LIVE);
    $LIVE = null;
}

function readSocket($len) {
    global $LIVE;
    $offset = 0;
    $socketData = '';

    while($offset < $len) {
        if(($data = @socket_read($LIVE, $len - $offset)) === false)
            return false;

        $dataLen = strlen ($data);
        $offset += $dataLen;
        $socketData .= $data;

        if($dataLen == 0)
            break;
    }

    return $socketData;
}

function queryLivestatus($query) {
    global $LIVE;

    // Query to get a json formated array back
    // Use fixed16 header
    socket_write($LIVE, $query . "OutputFormat:json\nResponseHeader: fixed16\n\n");

    // Read 16 bytes to get the status code and body size
    $read = readSocket(16);

    if($read === false)
        throw new LiveException('Problem while reading from socket: '.socket_strerror(socket_last_error($LIVE)));

    // Extract status code
    $status = substr($read, 0, 3);

    // Extract content length
    $len = intval(trim(substr($read, 4, 11)));

    // Read socket until end of data
    $read = readSocket($len);

    if($read === false)
        throw new LiveException('Problem while reading from socket: '.socket_strerror(socket_last_error($LIVE)));

    // Catch errors (Like HTTP 200 is OK)
    if($status != "200")
        throw new LiveException('Problem while reading from socket: '.$read);

    // Catch problems occured while reading? 104: Connection reset by peer
    if(socket_last_error($LIVE) == 104)
        throw new LiveException('Problem while reading from socket: '.socket_strerror(socket_last_error($LIVE)));

    // Decode the json response
    $obj = json_decode(utf8_encode($read));

    // json_decode returns null on syntax problems
    if($obj === null)
        throw new LiveException('The response has an invalid format');
    else
        return $obj;
}

function connectSocket() {
    global $conf, $LIVE;
    // Create socket connection
    if($conf['socketType'] === 'unix') {
        $LIVE = socket_create(AF_UNIX, SOCK_STREAM, 0);
    } elseif($conf['socketType'] === 'tcp') {
        $LIVE = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    }

    if($LIVE == false) {
        throw new LiveException('Could not create livestatus socket connection.');
    }

    // Connect to the socket
    if($conf['socketType'] === 'unix') {
        $result = socket_connect($LIVE, $conf['socketPath']);
    } elseif($conf['socketType'] === 'tcp') {
        $result = socket_connect($LIVE, $conf['socketAddress'], $conf['socketPort']);
    }

    if($result == false) {
        throw new LiveException('Unable to connect to livestatus socket.');
    }

    // Maybe set some socket options
    if($conf['socketType'] === 'tcp') {
        // Disable Nagle's Alogrithm - Nagle's Algorithm is bad for brief protocols
        if(defined('TCP_NODELAY')) {
            socket_set_option($LIVE, SOL_TCP, TCP_NODELAY, 1);
        } else {
            // See http://bugs.php.net/bug.php?id=46360
            socket_set_option($LIVE, SOL_TCP, 1, 1);
        }
    }
}

function checkSocketSupport() {
    if(!function_exists('socket_create'))
        throw new LiveException('The PHP function socket_create is not available. Maybe the sockets module is missing in your PHP installation.');
}

function checkSocketExists() {
    global $conf;
    if(!file_exists($conf['socketPath']))
        throw new LiveException('The configured livestatus socket does not exists');
}

// ----------------------------------------------------------------------------
//    MAIN FUNCTION
// ----------------------------------------------------------------------------
livestatusCom();

?>


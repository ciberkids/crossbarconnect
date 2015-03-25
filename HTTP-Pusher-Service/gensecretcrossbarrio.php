<?php
//curl -H "Content-Type: application/json" -d '{"topic": "com.tridas.statemachine.statechange", "args": [{"ciao":"mi sta simpatico"}]}' http://127.0.0.1:5555/


$key="test";
$secret="kkjH68GiuUZ";
$nonce=rand ( 0 , 2^53 );
$nonce = 10;

$t = microtime(true);
$micro = sprintf("%06d",($t - floor($t)) * 1000000);
$timestamp= new DateTime(date('Y-m-d H:i:s.'.$micro,$t));

//echo $timestamp->format('Y-m-d\TH:i:s.u\Z')."\n";

$timestamp->setTimeZone(new DateTimeZone("UTC"));

$formatedtimestamp = $timestamp->format('Y-m-d\TH:i:s.u\Z');
echo $timestamp->format('Y-m-d\TH:i:s.u\Z')."\n";
//$formatedtimestamp="2015-03-24T15:38:12.589Z";

$seq=1;
//$body="{"topic": "com.tridas.statemachine.statechange", "args": [{"ciao":"mi sta simpatico"}]}";

$body=array();
$body['topic'] = 'com.tridas.statemachine.statechange';
$body['args'] = array();
$argument=array();
$argument[] = array('test'=> 'funziona');

$body['args']= $argument;


$jsonbody = utf8_encode(json_encode($body));
$param = array();
$param['timestamp'] = $formatedtimestamp;
$param['seq'] = $seq;
$param['key'] = $key;
$param['nonce'] = $nonce;


$ctx = hash_init('sha256', HASH_HMAC, $secret);
echo "1-->". hash_final($ctx) . "\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);

echo "2-->" . hash_final($ctx)."\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);
hash_update($ctx, $formatedtimestamp);

echo "3-->".hash_final($ctx)."\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);
hash_update($ctx, $formatedtimestamp);
hash_update($ctx, $seq);

echo "4-->".hash_final($ctx)."\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);
hash_update($ctx, $formatedtimestamp);
hash_update($ctx, $seq);
hash_update($ctx, $nonce);

echo "5-->".hash_final($ctx)."\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);
hash_update($ctx, $formatedtimestamp);
hash_update($ctx, $seq);
hash_update($ctx, $nonce);
hash_update($ctx, $jsonbody);

$signature = hash_final($ctx);
echo "final-->".$signature."\n";

$ctx = hash_init('sha256', HASH_HMAC, $secret);
hash_update($ctx, $key);
hash_update($ctx, $formatedtimestamp);
hash_update($ctx, $seq);
hash_update($ctx, $nonce);
hash_update($ctx, $jsonbody);

$signature = hash_final($ctx, true);
$encodedsign = base64_encode($signature);
$encodedsign = str_replace(array('+','/'),array('-','_',''),$encodedsign);


$param['signature'] = $encodedsign; // rtrim(strtr(base64_encode($signature), '+/', '-_'), '=');

//var_dump($param);
echo "encode-->".$param['signature']."\n";
echo json_encode($body)."\n";
echo json_encode($param)."\n";

$path = "http://127.0.0.1:5555?" . http_build_query ($param );

echo $path . "\n";

echo "\ncurl -H \"Content-Type: application/json\" -d '" . json_encode($body) . "' \"". $path . "\"\n\n";

//set the url, number of POST vars, POST data
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $path);
curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));
curl_setopt($ch, CURLOPT_POST, count($body));
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 1);

$responce = curl_exec($ch);
$result = array( 'header' => '', 
                         'body' => '', 
                         'curl_error' => '', 
                         'http_code' => '',
                         'last_url' => '');
$output=$responce;

var_dump($output);

$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$header=substr($responce, 0, $header_size);
$body = substr( $responce, $header_size, strlen($responce) );
//storing result
$result['header'] = $header;
$result['http_code'] = curl_getinfo($ch,CURLINFO_HTTP_CODE);
$result['last_url'] = curl_getinfo($ch,CURLINFO_EFFECTIVE_URL);

if($result['http_code'] >= 500 ) {
  $result['body'] = array(  'action' => 'failed',
                            'reason' => 'remote services has replied with ' . $result['http_code'] . ' Error\n contact sysadmin',
                            'remote_url' => $result['last_url']
                          );
}
else $result['body'] = $body;

var_dump($result);
//close connection
curl_close($ch);



//ref for crossbar.io config

/**
{
   "controller": {
   },
   "workers": [
      {
         "type": "router",
         "realms": [
            {
               "name": "realm1",
               "roles": [
                  {
                     "name": "anonymous",
                     "permissions": [
                        {
                           "uri": "*",
                           "publish": false,
                           "subscribe": true,
                           "call": false,
                           "register": false
                        }
                     ]
                  },
                  {
                     "name": "server",
                     "permissions": [
                        {
                           "uri": "*",
                           "publish": true,
                           "subscribe": false,
                           "call": false,
                           "register": false
                        }
                     ]
                  }
               ]
            }
         ],
         "transports": [
            {
               "type": "websocket",
               "endpoint": {
                  "type": "tcp",
                  "port": 8080
               }
            },
            {
               "type": "web",
               "endpoint": {
                  "type": "tcp",
                  "port": 5555
               },
               "paths": {
                  "/": {
                     "type": "publisher",
                     "realm": "realm1",
                     "role": "server",
                     "options": {
                            "require_ip": ["127.0.0.1"]
                     	}
                  }
               }
            }
         ]
      }
   ]
}


**/









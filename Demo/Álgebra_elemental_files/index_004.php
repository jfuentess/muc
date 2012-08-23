// Using OpenStreetMap in Wikipedia.
// (c) 2008 by Magnus Manske
// Released under GPL
 
function openStreetMapToggle () {
  var osm_secure = '',
      c = document.getElementById ( 'coordinates' ) ;
  if ( !c ) return ;
  var cs = document.getElementById ( 'contentSub' ),
      osm = document.getElementById ( 'openstreetmap' ) ;
 
  if ( cs && osm ) {
    if ( osm.style.display == 'none' ) {
      osm.style.display = 'block' ;
    } else {
      osm.style.display = 'none' ;
    }
    return false ;
  }
 
  var found_link = false,
      a = c.getElementsByTagName ( 'a' ),
      h;
  for ( var i = 0 ; i < a.length ; i++ ) {
    h = a[i].href ;
    if ( !h.match( /geohack/ ) ) continue ;
    found_link = true ;
    break ;
  }
  if ( !found_link ) return ; // No geohack link found
 
  h = h.split('params=')[1] ;
 
  if ( window.location.protocol == 'https:' ) {
    osm_secure = '&secure=1' ;
  }
 
  var iframe = document.createElement ( 'iframe' ),
      url = '//toolserver.org/~kolossos/openlayers/kml-on-ol.php?lang=' + osm_proj_lang + '&uselang=' + wgUserLanguage + '&params=' + h + '&title=' + mw.util.wikiUrlencode( mw.config.get( 'wgTitle' ) ) + osm_secure ;
 
  iframe.id = 'openstreetmap' ;
  iframe.style.width = '100%' ;
  iframe.style.height = '350px' ;
  iframe.style.clear = 'both' ;
  iframe.src = url ;
  cs.appendChild ( iframe ) ;
  return false ;
}
 
function openStreetMapInit () {
  var c = document.getElementById ( 'coordinates' ) ;
  if ( !c ) return ;
 
  var a = c.getElementsByTagName ( 'a' ),
      geohack = false;
  for ( var i = 0 ; i < a.length ; i++ ) {
    var h = a[i].href ;
    if ( !h.match( /geohack/ ) ) continue ;
    geohack = true ;
    break ;
  }
  if ( !geohack ) return ;
 
  var na = document.createElement ( 'a' ) ;
  na.href = '#' ;
  na.onclick = openStreetMapToggle ;
  na.appendChild ( document.createTextNode ( osm_proj_map ) ) ;
  c.appendChild ( document.createTextNode ( ' (' ) ) ;
  c.appendChild ( na ) ;
  c.appendChild ( document.createTextNode ( ')   ' ) ) ;
}
 
$( openStreetMapInit ) ;
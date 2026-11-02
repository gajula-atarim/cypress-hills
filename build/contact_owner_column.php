// Cypress Hills — Contact page: move the owners' photo into its own column to the right of the form
// (run via Atarim execute-php). Uploads the full-height crop design/images/cypress-hills-owners-tall.jpg
// from the pinned commit (once), takes the photo out from under the Service Area card, sets the grid to
// 30% info cards | 45% form | 25% photo (100% each on tablet/phone), and updates the theme CSS.
// Re-running is safe: the upload is reused and the column is not added twice.
$ref = 'REF'; // replaced with the commit SHA when run
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$page = get_page_by_path( 'contact', OBJECT, 'page' );
if ( ! $page ) {
	throw new Exception( 'contact page not found' );
}
$alt = 'The owners of Cypress Hills Landscaping';
$ex  = get_posts( array( 'post_type' => 'attachment', 'name' => 'cypress-hills-owners-tall', 'post_status' => 'any', 'numberposts' => 1 ) );
if ( $ex ) {
	$aid = $ex[0]->ID;
} else {
	$tmp = download_url( 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/design/images/cypress-hills-owners-tall.jpg', 30 );
	if ( is_wp_error( $tmp ) ) {
		throw new Exception( 'download failed: ' . $tmp->get_error_message() );
	}
	$aid = media_handle_sideload( array( 'name' => 'cypress-hills-owners-tall.jpg', 'tmp_name' => $tmp ), $page->ID, 'Cypress Hills owners' );
	if ( is_wp_error( $aid ) ) {
		@unlink( $tmp );
		throw new Exception( 'upload failed: ' . $aid->get_error_message() );
	}
}
update_post_meta( $aid, '_wp_attachment_image_alt', $alt );

$pct = function ( $n ) {
	return array( 'unit' => '%', 'size' => $n, 'sizes' => array() );
};
$has = function ( $el, $cls ) {
	$c = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : ( isset( $el['settings']['css_classes'] ) ? $el['settings']['css_classes'] : '' );
	return (bool) preg_match( '/(^|\s)' . preg_quote( $cls, '/' ) . '(\s|$)/', $c );
};
$column = array(
	'id'       => substr( md5( 'ch-owner-col' ), 0, 7 ),
	'elType'   => 'container',
	'isInner'  => true,
	'settings' => array(
		'content_width'  => 'full',
		'flex_direction' => 'column',
		'flex_gap'       => array( 'column' => '0', 'row' => '0', 'isLinked' => true, 'unit' => 'px', 'size' => 0 ),
		'padding'        => array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '0', 'left' => '0', 'isLinked' => true ),
		'width'          => $pct( 25 ),
		'width_tablet'   => $pct( 100 ),
		'css_classes'    => 'ch-owner-col',
	),
	'elements' => array(
		array(
			'id'         => substr( md5( 'ch-owner-photo' ), 0, 7 ),
			'elType'     => 'widget',
			'widgetType' => 'image',
			'isInner'    => false,
			'settings'   => array(
				'image'        => array( 'id' => $aid, 'url' => wp_get_attachment_url( $aid ), 'alt' => $alt, 'source' => 'library' ),
				'image_size'   => 'full',
				'width'        => $pct( 100 ),
				'_css_classes' => 'ch-media ch-owner-photo',
			),
			'elements'   => array(),
		),
	),
);

$state = array( 'grid' => false, 'col' => false );
$walk  = function ( $els ) use ( &$walk, $has, $column, $pct, &$state ) {
	$out = array();
	foreach ( $els as $el ) {
		// The earlier photo under the Service Area card goes; the new column carries it now.
		if ( 'widget' === $el['elType'] && $has( $el, 'ch-owner-photo' ) ) {
			continue;
		}
		if ( $has( $el, 'ch-owner-col' ) ) {
			$state['col'] = true;
			$out[]        = $column; // refresh in place on a re-run
			continue;
		}
		if ( ! empty( $el['elements'] ) ) {
			$kids = $el['elements'];
			$is_grid = false;
			foreach ( $kids as $k ) {
				if ( $has( $k, 'ch-form-card' ) ) {
					$is_grid = true;
				}
			}
			if ( $is_grid ) {
				$state['grid'] = true;
				foreach ( $kids as $i => $k ) {
					if ( $has( $k, 'ch-form-card' ) ) {
						$kids[ $i ]['settings']['width'] = $pct( 45 );
					} elseif ( ! $has( $k, 'ch-owner-col' ) ) {
						$kids[ $i ]['settings']['width'] = $pct( 30 ); // info cards column
					}
				}
			}
			$el['elements'] = $walk( $kids );
			if ( $is_grid && ! $state['col'] ) {
				$el['elements'][] = $column;
				$state['col']     = true;
			}
		}
		$out[] = $el;
	}
	return $out;
};
$doc  = \Elementor\Plugin::$instance->documents->get( $page->ID, false );
$data = $walk( $doc->get_elements_data() );
if ( ! $state['grid'] ) {
	throw new Exception( 'form grid not found' );
}
$doc->save( array( 'elements' => $data ) );

$rel = 'assets/css/cypress-hills.css';
$r   = wp_remote_get( 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/wp-content/themes/hello-elementor-child/' . $rel, array( 'timeout' => 30 ) );
if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
	throw new Exception( 'css fetch failed' );
}
file_put_contents( get_stylesheet_directory() . '/' . $rel, wp_remote_retrieve_body( $r ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'attachment' => $aid, 'url' => wp_get_attachment_url( $aid ), 'css' => sha1_file( get_stylesheet_directory() . '/' . $rel ) ) );

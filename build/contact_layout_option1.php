// Cypress Hills — Contact page "option 1" layout (run via Atarim execute-php).
// Left column (45%): owners' photo on top, Phone + Hours side by side, then Service Area. Right column
// (55%): the form card. The separate photo column is removed. Existing cards keep their content and
// settings; they are only regrouped. Updates the theme CSS from the same commit.
$ref = 'REF'; // replaced with the commit SHA when run

$page = get_page_by_path( 'contact', OBJECT, 'page' );
if ( ! $page ) {
	throw new Exception( 'contact page not found' );
}
$ex = get_posts( array( 'post_type' => 'attachment', 'name' => 'cypress-hills-owners', 'post_status' => 'any', 'numberposts' => 1 ) );
if ( ! $ex ) {
	throw new Exception( 'cypress-hills-owners.jpg not in media library' );
}
$aid = $ex[0]->ID;
$alt = 'The owners of Cypress Hills Landscaping';

$pct = function ( $n ) {
	return array( 'unit' => '%', 'size' => $n, 'sizes' => array() );
};
$has = function ( $el, $cls ) {
	$c = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : ( isset( $el['settings']['css_classes'] ) ? $el['settings']['css_classes'] : '' );
	return (bool) preg_match( '/(^|\s)' . preg_quote( $cls, '/' ) . '(\s|$)/', $c );
};
$photo = array(
	'id'         => substr( md5( 'ch-owner-photo-o1' ), 0, 7 ),
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
);
$zero = array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '0', 'left' => '0', 'isLinked' => true );

$done = array( 'grid' => false );
$walk = function ( $els ) use ( &$walk, $has, $pct, $photo, $zero, &$done ) {
	foreach ( $els as $i => $el ) {
		if ( empty( $el['elements'] ) ) {
			continue;
		}
		$is_grid = false;
		foreach ( $el['elements'] as $k ) {
			if ( $has( $k, 'ch-form-card' ) ) {
				$is_grid = true;
			}
		}
		if ( ! $is_grid ) {
			$els[ $i ]['elements'] = $walk( $el['elements'] );
			continue;
		}
		$done['grid'] = true;
		$info = null;
		$form = null;
		foreach ( $el['elements'] as $k ) {
			if ( $has( $k, 'ch-form-card' ) ) {
				$form = $k;
			} elseif ( ! $has( $k, 'ch-owner-col' ) ) {
				$info = $k; // the photo column (ch-owner-col) is dropped
			}
		}
		if ( ! $info || ! $form ) {
			throw new Exception( 'grid columns not found' );
		}
		$phone = $hours = $area = null;
		$walk_cards = function ( $kids ) use ( &$walk_cards, $has, &$phone, &$hours, &$area ) {
			foreach ( $kids as $c ) {
				if ( 'widget' === $c['elType'] ) {
					continue; // the old photo under Service Area, if any
				}
				if ( $has( $c, 'ch-contact-duo' ) ) {
					$walk_cards( $c['elements'] ); // re-run: unpack the existing pair
				} elseif ( $has( $c, 'ch-phone-card' ) ) {
					$phone = $c;
				} elseif ( $has( $c, 'ch-area-card' ) ) {
					$area = $c;
				} else {
					$hours = $c;
				}
			}
		};
		$walk_cards( $info['elements'] );
		if ( ! $phone || ! $hours || ! $area ) {
			throw new Exception( 'info cards not found' );
		}
		$duo = array(
			'id'       => substr( md5( 'ch-contact-duo' ), 0, 7 ),
			'elType'   => 'container',
			'isInner'  => true,
			'settings' => array(
				'content_width'  => 'full',
				'flex_direction' => 'row',
				'flex_gap'       => array( 'column' => '16', 'row' => '16', 'isLinked' => true, 'unit' => 'px', 'size' => 16 ),
				'padding'        => $zero,
				'css_classes'    => 'ch-contact-duo',
			),
			'elements' => array( $phone, $hours ),
		);
		$info['elements']                  = array( $photo, $duo, $area );
		$info['settings']['width']         = $pct( 45 );
		$info['settings']['width_tablet']  = $pct( 100 );
		$form['settings']['width']         = $pct( 55 );
		$form['settings']['width_tablet']  = $pct( 100 );
		$els[ $i ]['elements']             = array( $info, $form );
	}
	return $els;
};
$doc  = \Elementor\Plugin::$instance->documents->get( $page->ID, false );
$data = $walk( $doc->get_elements_data() );
if ( ! $done['grid'] ) {
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
echo wp_json_encode( array( 'photo' => $aid, 'css' => sha1_file( get_stylesheet_directory() . '/' . $rel ) ) );

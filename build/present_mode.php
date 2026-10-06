// Cypress Hills — "present the Home page only" mode (run via Atarim execute-php).
// Points every link to another page at "#" in the Site Header, Site Footer and Home page, and turns
// the Primary Menu items (except Home) into "#" links. No page is deleted or edited.
// Kept as-is: Home ("/"), the logo, tel:, social links, on-page anchors (#book) and images.
// To bring the real links back, re-run build/setup_pages.php (it rebuilds header, footer, home and menu).
$home_url = trailingslashit( home_url() );
$is_page_link = function ( $u ) use ( $home_url ) {
	if ( ! is_string( $u ) || '' === $u ) {
		return false;
	}
	if ( 0 === strpos( $u, $home_url ) ) {
		$u = '/' . substr( $u, strlen( $home_url ) );
	}
	if ( '/' === $u || 0 !== strpos( $u, '/' ) || 0 === strpos( $u, '//' ) ) {
		return false;
	}
	return ! preg_match( '#^/wp-content/#', $u );
};
$changed = 0;
$walk    = function ( $node ) use ( &$walk, $is_page_link, &$changed ) {
	if ( ! is_array( $node ) ) {
		return $node;
	}
	foreach ( $node as $k => $v ) {
		if ( 'url' === $k && $is_page_link( $v ) ) {
			$node[ $k ] = '#';
			$changed++;
		} elseif ( is_string( $v ) && false !== strpos( $v, 'href=' ) ) {
			// Inline links inside text: href='/services/' or href="/services/".
			$node[ $k ] = preg_replace_callback(
				'#href=(["\'])([^"\']*)\1#',
				function ( $m ) use ( $is_page_link, &$changed ) {
					if ( $is_page_link( $m[2] ) ) {
						$changed++;
						return 'href=' . $m[1] . '#' . $m[1];
					}
					return $m[0];
				},
				$v
			);
		} elseif ( is_array( $v ) ) {
			$node[ $k ] = $walk( $v );
		}
	}
	return $node;
};
$find = function ( $type, $title ) {
	$p = get_posts( array( 'post_type' => $type, 'title' => $title, 'post_status' => 'any', 'numberposts' => 1 ) );
	return $p ? $p[0]->ID : 0;
};
$docs = \Elementor\Plugin::$instance->documents;
$out  = array();
foreach ( array(
	'header' => $find( 'elementor-hf', 'Site Header' ),
	'footer' => $find( 'elementor-hf', 'Site Footer' ),
	'home'   => (int) get_option( 'page_on_front' ),
) as $name => $id ) {
	$doc  = $docs->get( $id, false );
	$data = $doc->get_elements_data();
	$changed = 0;
	$data = $walk( $data );
	if ( $changed ) {
		$doc->save( array( 'elements' => $data ) );
	}
	$out[ $name ] = $changed;
}

// Primary Menu: everything except Home becomes a "#" custom link (titles, nesting and classes kept).
$menu  = wp_get_nav_menu_object( 'Primary Menu' );
$front = (int) get_option( 'page_on_front' );
$n     = 0;
foreach ( (array) wp_get_nav_menu_items( $menu->term_id ) as $it ) {
	if ( ( 'post_type' === $it->type && (int) $it->object_id === $front ) || '#' === $it->url ) {
		continue;
	}
	wp_update_nav_menu_item( $menu->term_id, $it->ID, array(
		'menu-item-type'      => 'custom',
		'menu-item-url'       => '#',
		'menu-item-title'     => $it->title,
		'menu-item-parent-id' => (int) $it->menu_item_parent,
		'menu-item-position'  => (int) $it->menu_order,
		'menu-item-classes'   => implode( ' ', array_filter( (array) $it->classes ) ),
		'menu-item-status'    => 'publish',
	) );
	$n++;
}
$out['menu'] = $n;
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( $out );

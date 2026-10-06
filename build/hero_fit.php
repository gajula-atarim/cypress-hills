// Cypress Hills — framing for individual Home banner photos (run via Atarim execute-php).
// Adds a CSS class to a slide's image widget (see "Banner photo framing" in the theme CSS); for "ch-fit"
// it also sets the widget's background to the same photo, which the CSS blurs behind the uncropped image.
$frame = array( 3 => 'ch-fit', 6 => 'ch-pos-top' );  // slide number => class
$home  = (int) get_option( 'page_on_front' );
$doc   = \Elementor\Plugin::$instance->documents->get( $home, false );
$n     = 0;
$out   = array();
$walk  = function ( $els ) use ( &$walk, &$n, $frame, &$out ) {
	foreach ( $els as $k => $el ) {
		$s   = isset( $el['settings'] ) ? $el['settings'] : array();
		$cls = isset( $s['_css_classes'] ) ? $s['_css_classes'] : '';
		if ( isset( $el['widgetType'] ) && 'image' === $el['widgetType'] && preg_match( '/(^|\s)ch-slide-img(\s|$)/', $cls ) ) {
			$n++;
			$parts = array_diff( preg_split( '/\s+/', trim( $cls ) ), array( 'ch-fit', 'ch-pos-top' ) );
			unset( $s['_background_background'], $s['_background_image'] );
			if ( isset( $frame[ $n ] ) ) {
				$parts[] = $frame[ $n ];
				if ( 'ch-fit' === $frame[ $n ] ) {
					$s['_background_background'] = 'classic';
					$s['_background_image']      = array( 'id' => $s['image']['id'], 'url' => $s['image']['url'], 'source' => 'library' );
				}
				$out[ $n ] = $frame[ $n ];
			}
			$s['_css_classes']        = implode( ' ', $parts );
			$els[ $k ]['settings']    = $s;
		}
		if ( ! empty( $el['elements'] ) ) {
			$els[ $k ]['elements'] = $walk( $el['elements'] );
		}
	}
	return $els;
};
$data = $walk( $doc->get_elements_data() );
if ( 7 !== $n ) {
	throw new Exception( 'expected 7 banner slides, found ' . $n );
}
$doc->save( array( 'elements' => $data ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'slides' => $n, 'framed' => $out ) );

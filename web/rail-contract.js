// Canonical source tag plus legacy fixture alias. Both refer to Uijeongbu VAL.
export const isLightRail = route => route.line === 'uijeongbu' || route.line === 'uline';
// Existing v18 geometry datum, not surveyed terrain elevations.
// Mainline detailed rail cap: .19 + .205 + .055/2 = .4225 m.
// New beam top .2 + .15/2 = .275 m, hence a .1475 m layer correction.
export const railLayerHeight = route => isLightRail(route) ? 7 : .1475;

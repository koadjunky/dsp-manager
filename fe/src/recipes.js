
const recipes = [
    {
        label: 'Fractinator',
        value: 'fractinator'
    },
    {
        label: 'Water Pump',
        value: 'water_pump'
    },
    {
        label: 'Water Pump',
        value: 'water_pump'
    },
    {
        label: 'Sulfric Acid Pump',
        value: 'sulfric_acid_pump'
    },
    {
        label: 'Oil Extractor',
        value: 'oil_extractor'
    },
    {
        label: 'Orbital Collector',
        value: 'orbital_collector'
    },
    {
        label: 'Coal Vein',
        value: 'coal_vein'
    },
    {
        label: 'Copper Ore Vein',
        value: 'copper_ore_vein'
    },
    {
        label: 'Fire Ice Vein',
        value: 'fire_ice_vein'
    },
    {
        label: 'Fractal Silicon Vein',
        value: 'fractal_silicon_vein'
    },
    {
        label: 'Iron Ore Vein',
        value: 'iron_ore_vein'
    },
    {
        label: 'Kimberlite Ore Vein',
        value: 'kimberlite_ore_vein'
    },
    {
        label: 'Optical Grating Crystal Vein',
        value: 'optical_grating_crystal_vein'
    },
    {
        label: 'Organic Crystal Vein',
        value: 'organic_crystal_vein'
    },
    {
        label: 'Silicon Ore Vein',
        value: 'silicon_ore_vein'
    },
    {
        label: 'Spinform Stalagmite Crystal Vein',
        value: 'spinform_stalagmite_crystal_vein'
    },
    {
        label: 'Stone Vein',
        value: 'stone_vein'
    },
    {
        label: 'Titanium Ore Vein',
        value: 'titanium_ore_vein'
    },
    {
        label: 'Unipolar Magnet Vein',
        value: 'unipolar_magnet_vein'
    },
    {
        label: 'Gear',
        value: 'gear'
    },
    {
        label: 'Magnetic Coil',
        value: 'magnetic_coil'
    },
    {
        label: 'Prism',
        value: 'prism'
    },
    {
        label: 'Plasma Exciter',
        value: 'plasma_exciter'
    },
    {
        label: 'Titanium Crystal',
        value: 'titanium_crystal'
    },
    {
        label: 'Casimir Crystal',
        value: 'casimir_crystal'
    },
    {
        label: 'Casimir Crystal *',
        value: 'casimir_crystal_plus'
    },
    {
        label: 'Titanium Glass',
        value: 'titanium_glass'
    },
    {
        label: 'Patricle Broadband',
        value: 'patricle_broadband'
    },
    {
        label: 'Plane Filter',
        value: 'plane_filter'
    },
    {
        label: 'Deuteron Fuel Rod',
        value: 'deuteron_fuel_rod'
    },
    {
        label: 'Annihilation Constraint Sphere',
        value: 'annihilation_constraint_sphere'
    },
    {
        label: 'Circuit Board',
        value: 'circuit_board'
    },
    {
        label: 'Processor',
        value: 'processor'
    },
    {
        label: 'Quantum Chip',
        value: 'quantum_chip'
    },
    {
        label: 'Microcrystalline Component',
        value: 'microcrystalline_component'
    },
    {
        label: 'Crystal Silicon *',
        value: 'crystal_silicon_plus'
    },
    {
        label: 'Photon Combiner',
        value: 'photon_combiner'
    },
    {
        label: 'Photon Combiner *',
        value: 'photon_combiner_plus'
    },
    {
        label: 'Solar Sail',
        value: 'solar_sail'
    },
    {
        label: 'Frame Material',
        value: 'frame_material'
    },
    {
        label: 'Dyson Sphere Component',
        value: 'dyson_sphere_component'
    },
    {
        label: 'Small Carrier Rocket',
        value: 'small_carrier_rocket'
    },
    {
        label: 'Electric Motor',
        value: 'electric_motor'
    },
    {
        label: 'Electromagnetic Turbine',
        value: 'electromagnetic_turbine'
    },
    {
        label: 'Patricle Container',
        value: 'patricle_container'
    },
    {
        label: 'Patricle Container *',
        value: 'patricle_container_plus'
    },
    {
        label: 'Graviton Lens',
        value: 'graviton_lens'
    },
    {
        label: 'Super Magnetic Ring',
        value: 'super_magnetic_ring'
    },
    {
        label: 'Iron Ingot',
        value: 'iron_ingot'
    },
    {
        label: 'Magnet',
        value: 'magnet'
    },
    {
        label: 'Copper Ingot',
        value: 'copper_ingot'
    },
    {
        label: 'Stone Brick',
        value: 'stone_brick'
    },
    {
        label: 'Energetic Graphite',
        value: 'energetic_graphite'
    },
    {
        label: 'Silicon Ore',
        value: 'silicon_ore'
    },
    {
        label: 'Crystal Silicon',
        value: 'crystal_silicon'
    },
    {
        label: 'Glass',
        value: 'glass'
    },
    {
        label: 'High Purity Silicon',
        value: 'high_purity_silicon'
    },
    {
        label: 'Diamond',
        value: 'diamond'
    },
    {
        label: 'Diamond *',
        value: 'diamond_plus'
    },
    {
        label: 'Steel',
        value: 'steel'
    },
    {
        label: 'Titanium Ingot',
        value: 'titanium_ingot'
    },
    {
        label: 'Titanium Alloy',
        value: 'titanium_alloy'
    },
    {
        label: 'Oil Refining',
        value: 'refining'
    },
    {
        label: 'X-Ray Cracking',
        value: 'x_ray_cracking'
    },
    {
        label: 'Deuterium',
        value: 'deuterium'
    },
    {
        label: 'Antimatter',
        value: 'antimatter'
    },
    {
        label: 'Strange Matter',
        value: 'strange_matter'
    },
    {
        label: 'Plastic',
        value: 'plastic'
    },
    {
        label: 'Sulfric Acid',
        value: 'sulfric_acid'
    },
    {
        label: 'Organic Crystal',
        value: 'organic_crystal'
    },
    {
        label: 'Graphene',
        value: 'graphene'
    },
    {
        label: 'Graphene *',
        value: 'graphene_plus'
    },
    {
        label: 'Carbon Nanotube',
        value: 'carbon_nanotube'
    },
    {
        label: 'Carbon Nanotube *',
        value: 'carbon_nanotube_plus'
    },
    {
        label: 'Blue Science',
        value: 'blue_science'
    },
    {
        label: 'Red Science',
        value: 'red_science'
    },
    {
        label: 'Yellow Science',
        value: 'yellow_science'
    },
    {
        label: 'Purple Science',
        value: 'purple_science'
    },
    {
        label: 'Green Science',
        value: 'green_science'
    },
    {
        label: 'White Science',
        value: 'white_science'
    }
];

export { recipes }

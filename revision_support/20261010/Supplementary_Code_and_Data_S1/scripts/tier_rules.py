"""Executable reconstruction of the historical, AI-assisted classification rules.

These rules were developed with knowledge of the initial classifications; they
are NOT a blinded or independent-rater study. At execution, the classifier
reads descriptive metadata only. The comparison labels are loaded separately.
The implementation follows the recorded branch logic, including source-specific
exceptions. It does not establish the scientific correctness of a Tier.
"""
from __future__ import annotations
import re
from typing import Mapping
TIERS = ('A_strict_direct','B_condition_resolved_direct','C_transparent_derived',
         'D_empirical_contextual_auxiliary','E_engineered_arithmetic_auxiliary',
         'F_relational_pair_auxiliary','G_noninterpretable_representation')
A,B,C,D,E,F,G=TIERS
LEARNED={'emb_cgcnn','emb_cgnf','emb_chemeleon','emb_chgnet','emb_crystallm',
         'emb_mace_mp0','emb_mat2vec','emb_matscholar','emb_matscibert',
         'emb_megnet16','emb_orb_v2','emb_sevennet','emb_skipatom'}
DERIVED={'mendeleev_derived','mendeleev_effective_nuclear_charge',
         'mendeleev_electronegativity_extended','mendeleev_ionic_radius',
         'mendeleev_isotope_decay_modes','mendeleev_isotope_extended',
         'mendeleev_li_xue_summary','mendeleev_oxidation','mendeleev_phase'}
DIRECT_B={'nist_atomic_orbital_lda','nist_neutron_natural_element',
          'xraydb_absorption_edges','xraydb_emission_lines','xraydb_mass_attenuation'}

def classify(r: Mapping[str,str]) -> tuple[str,str]:
    """Return (Tier, rule identifier); never access initial/adopted Tier labels."""
    b,n=r['feature_block'],r['feature_name']
    if b in LEARNED:return G,'R01_encoded_or_learned_block'
    if b=='emb_mod_petti':return D,'R02_ordering_scale'
    if b=='emb_magpie22':
        return (D,'R03_magpie_ordering') if n.endswith('__MendeleevNumber') else (A,'R03_named_magpie_property')
    if b=='emb_oliynyk44':
        if n.endswith(('__Zunger_radii_sum','__outer_shell_electrons')):return C,'R04_oliynyk_arithmetic_count'
        if n.endswith(('__Mendeleev_Number','__Miracle_Radius_pm')):return D,'R04_oliynyk_empirical'
        return A,'R04_oliynyk_named'
    if b=='matminer_jarvis':
        if any(x in n for x in ('_add_','_mult_','_subs_','_divi_')):return E,'R05_jarvis_arithmetic'
        if re.search(r'__C-\d+$',n):return B,'R05_jarvis_tensor_component'
        if n in {'jarvis_cfid__GV','jarvis_cfid__KV','jarvis_cfid__avg_ion_rad','jarvis_cfid__max_oxid_s','jarvis_cfid__min_oxid_s'}:return C,'R05_jarvis_summary'
        return A,'R05_jarvis_named'
    if b=='matminer_miedema':
        return (F,'R06_partner_aggregate') if n.startswith('miedema_pair__') else (D,'R06_model_parameter')
    if b=='mendeleev_element':
        contextual=('__series_id','__abundance_','__discovery_year','__mendeleev_number','__pettifor_number','__glawe_number',
                    '__production_','__relative_supply_risk','__reserve_','__political_stability_','__price_per_kg',
                    '__geochemical_class__','__goldschmidt_class__','__substitutability__','__recycling_rate__',
                    '__en_miedema','__miedema_molar_volume','__miedema_electron_density')
        return (D,'R07_contextual_or_model') if any(x in n for x in contextual) else (A,'R07_named_element')
    if b=='mendeleev_electron_configuration':return C,'R08_parsed_occupancy'
    if b in DERIVED:return C,'R09_formula_or_aggregate'
    if b=='mendeleev_isotope':return (D,'R10_historical_year') if 'discovery_year' in n else (C,'R10_isotope_aggregate')
    if b=='mendeleev_ionization':return (B,'R11_stage_value_or_flag') if '__stage_' in n else (C,'R11_cumulative_or_summary')
    if b=='mendeleev_ionization_uncertainty':
        return (B,'R12_absolute_stage_uncertainty') if '__stage_' in n and n.endswith('_uncertainty_eV') else (C,'R12_relative_or_summary_uncertainty')
    if b=='mendeleev_ionization_state':return B,'R13_charge_resolved_term'
    if b in {'mendeleev_scattering_factors','mendeleev_screening'}:return B,'R14_energy_or_orbital'
    if b in DIRECT_B:return B,'R15_source_resolved_quantity'
    if b in {'nist_atomic_orbital_lda_derived','nist_neutron_natural_element_derived'}:return C,'R16_nist_summary_or_ratio'
    if b=='ciaaw_standard_atomic_weights_2024':
        return (A,'R17_ciaaw_flag') if any(x in n for x in ('__is_interval_','__has_standard_','__footnote_')) else (C,'R17_ciaaw_parsed_interval')
    if b=='matminer_deml':
        if '__ionization_energy_' in n or '__charge_pos' in n:return B,'R18_stage_or_charge'
        if '__charge_state_has_' in n or '_from_column' in n:return C,'R18_flag_or_valence_count'
        if n=='deml__mus_fere':return D,'R18_fitted_reference'
        return A,'R18_deml_named'
    if b=='matminer_magpie':
        if 'OxidationStates_' in n:return C,'R19_oxidation_set_summary'
        if 'IonizationEnergies_' in n or n.endswith('__SecondIonizationEnergy'):return B,'R19_ionization_stage'
        if n.endswith('__LogThermalConductivity'):return C,'R19_log_transform'
        if any(n.endswith('__'+x) for x in ('HHIp','HHIr','MendeleevNumber','MiracleRadius','phi','n_ws_pow_third')):return D,'R19_contextual_model'
        return A,'R19_magpie_named'
    if b=='matminer_cohesive':return A,'R20_cohesive_energy'
    if b=='xenonpy_original':return (D,'R21_xenonpy_ordering') if n=='mendeleev_number' else (A,'R21_xenonpy_tabulated')
    if r.get('formula','').strip() or r.get('input_features','').strip():return C,'R22_fallback_formula'
    if any(r.get(k,'').strip() for k in ('charge_state','isotope_mass_number','photon_energy_eV','electron_energy_eV','wavelength_nm','miller_index')):return B,'R23_fallback_condition'
    return A,'R24_fallback_named'

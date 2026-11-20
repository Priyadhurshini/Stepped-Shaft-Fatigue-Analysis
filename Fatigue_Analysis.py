import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. SHAFT GEOMETRY & LOADING PARAMETERS
# ==========================================
D = 40.0       # Large diameter (mm)
d = 20.0       # Small diameter (mm)
M = 100000.0   # Bending moment (N*mm)

# Fillet radii from FEA parametric sweep (mm)
r_sweep = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

# ==========================================
# 2. ANALYTICAL BENDING & NOTCH CALCULATIONS
# ==========================================
# Nominal Bending Stress (MPa) on small diameter
sigma_nom = (32.0 * M) / (np.pi * (d**3))

# Peterson's Stress Concentration Factor Kt approximation for r/d
# Kt formula approximation for D/d = 2.0 stepped shaft in bending
r_over_d = r_sweep / d
Kt_analytical = 1.0 + 0.22 * (r_over_d)**(-0.45)
sigma_analytical = Kt_analytical * sigma_nom

# Exact peak stress values from your Ansys Design Point table:
sigma_fea = np.array([256.79, 207.4, 185.62, 172.14, 163.26]) 

# ==========================================
# 3. FATIGUE LIFE EVALUATION (S-N CURVE)
# ==========================================
S_ut = 600.0   # Ultimate tensile strength for structural steel (MPa)
S_e = 0.5 * S_ut * 0.8  # Endurance limit (~240 MPa with surface/size factors)

# Basquin's Equation for finite life calculation (10^3 to 10^6 cycles)
f = 0.9
a = (f * S_ut)**2 / S_e
b = -(1/3) * np.log10((f * S_ut) / S_e)

# Calculation of predicted cycles for 2 mm fillet peak stress
peak_stress_2mm = sigma_fea[1] # ~230 MPa
N_cycles = (peak_stress_2mm / a)**(1/b)

print(f"--- ANALYTICAL & FEA RESULTS SUMMARY ---")
print(f"Nominal Bending Stress (sigma_nom) : {sigma_nom:.2f} MPa")
print(f"2mm Fillet Peak FEA Stress         : {peak_stress_2mm:.2f} MPa")
print(f"Calculated Fatigue Life (N)        : {int(N_cycles):,} cycles")
print("---------------------------------------")

# ==========================================
# 4. PLOTTING: FEA VS ANALYTICAL STRESS SWEEP
# ==========================================
plt.figure(figsize=(8, 5))
plt.plot(r_sweep, sigma_analytical, 'r--o', label='Analytical Notch Stress ($K_t \\cdot \\sigma_{nom}$)', linewidth=2)
plt.plot(r_sweep, sigma_fea, 'b-s', label='Ansys FEA Peak von Mises Stress', linewidth=2)

plt.axhline(y=sigma_nom, color='gray', linestyle=':', label=f'Nominal Stress ({sigma_nom:.1f} MPa)')
plt.title('Stepped Shaft: Fillet Radius vs. Peak Stress Concentration', fontsize=12, fontweight='bold')
plt.xlabel('Fillet Radius r (mm)', fontsize=10)
plt.ylabel('Peak von Mises Stress (MPa)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Save plot
plt.savefig('stepped_shaft_fatigue_sweep.png', dpi=300)
plt.show()
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'outputs' / 'summary_results_2022_2025.csv'
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)

# Read the already-derived reproducible summary and select the 2022-2025 aggregate rows.
df = pd.read_csv(DATA)
agg = df[df['year'].astype(str).eq('2022-2025')].set_index('source')

# Panel a: AI grants as a share of all NHMRC/MRFF grants.
a = pd.DataFrame({
    'funder': ['NHMRC', 'MRFF'],
    'numerator': [agg.loc['NHMRC', 'ai_grant_count'], agg.loc['MRFF', 'ai_grant_count']],
    'denominator': [agg.loc['NHMRC', 'total_grant_count'], agg.loc['MRFF', 'total_grant_count']],
})
a['proportion'] = a['numerator'] / a['denominator']

# Panel b: ARC AI grants that also meet the molecular/life-science screen.
b = pd.DataFrame({
    'funder': ['ARC'],
    'numerator': [agg.loc['ARC', 'ai_mls_grant_count']],
    'denominator': [agg.loc['ARC', 'ai_grant_count']],
})
b['proportion'] = b['numerator'] / b['denominator']

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 17,
    'axes.titlesize': 20,
    'axes.labelsize': 18,
    'xtick.labelsize': 18,
    'ytick.labelsize': 16,
})

fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(13.5, 7.5),
    gridspec_kw={'width_ratios': [1.0, 0.62], 'wspace': 0.34},
)

bar_color = '#315F86'

# Panel a
bars1 = ax1.bar(a['funder'], a['proportion'], width=0.58, color=bar_color)
ax1.set_xlim(-0.6, 1.6)
ax1.set_ylabel('Proportion of grants')
ax1.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
ax1.set_ylim(0, 0.026)
ax1.grid(axis='y', alpha=0.22, linewidth=1.0)
ax1.set_axisbelow(True)
ax1.text(-0.12, 1.10, 'a)', transform=ax1.transAxes, fontsize=24, fontweight='bold', va='top')

for bar, row in zip(bars1, a.itertuples(index=False)):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    ax1.text(
        x, y + 0.00055,
        f'{int(row.numerator):,} / {int(row.denominator):,}\n{row.proportion:.1%}',
        ha='center', va='bottom', fontsize=17, fontweight='semibold', linespacing=1.15,
    )

# Panel b
# Match the physical bar width in panel a. With the 0.62 subplot-width ratio
# and explicit x-limits below, width=0.51 renders at the same width as 0.58 in panel a.
bars2 = ax2.bar(b['funder'], b['proportion'], width=0.51, color=bar_color)
ax2.set_xlim(-0.6, 0.6)
ax2.set_ylabel('Proportion of AI grants')
ax2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax2.set_ylim(0, 0.105)
ax2.grid(axis='y', alpha=0.22, linewidth=1.0)
ax2.set_axisbelow(True)
ax2.text(-0.19, 1.10, 'b)', transform=ax2.transAxes, fontsize=24, fontweight='bold', va='top')

for bar, row in zip(bars2, b.itertuples(index=False)):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    ax2.text(
        x, y + 0.0030,
        f'{int(row.numerator):,} / {int(row.denominator):,}\n{row.proportion:.1%}',
        ha='center', va='bottom', fontsize=17, fontweight='semibold', linespacing=1.15,
    )

for ax in (ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.1)
    ax.spines['bottom'].set_linewidth(1.1)
    ax.tick_params(axis='x', length=0, pad=8)
    ax.tick_params(axis='y', width=1.0)

fig.suptitle('AI + molecular/life-science grant proportions, 2022–2025', fontsize=24, fontweight='semibold', y=0.985)
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.10, right=0.98)

for ext in ('png', 'svg', 'pdf'):
    path = OUT / f'grant_proportions_2022_2025.{ext}'
    fig.savefig(path, dpi=300 if ext == 'png' else None, bbox_inches='tight')

print(a.to_string(index=False))
print(b.to_string(index=False))

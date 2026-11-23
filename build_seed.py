import csv,json,re
from pathlib import Path
root=Path('/mnt/data/equi_allocator_intelligence_v1')
source=Path('/mnt/data/apollo-accounts-export(1).csv')
with source.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
SCORE=next(k for k in rows[0] if k.startswith('Equi Platform Fit Score'))
# Source-verified evidence is narrowly worded. Unverified notes are labeled and never scored as verified.
P={
 'Maridea Wealth Management':dict(
  unknowns=['Current willingness to add or replace external alternatives providers','Who approves fund-platform partnerships and which strategies are priorities'],
  analyst='Potential partner fit: disclosed independent-manager use plus a growing wealth platform. Evidence does not establish current purchasing intent.',
  stage='Research priority',
  evidence=[
   dict(title='Independent-manager relationships disclosed',detail='Maridea describes referring clients to independent managers and the associated service and billing arrangements.',url='https://marideawealth.com/wp-content/uploads/2026/10/ADV2A_Maridea_20260930.pdf',date='2026-09-30',kind='positive',points=23,verified=True,type='Firm Form ADV brochure'),
   dict(title='Approximately $1.97B in client assets',detail='Firm brochure states $1,971,582,760 client assets under management as of August 31, 2026.',url='https://marideawealth.com/wp-content/uploads/2026/10/ADV2A_Maridea_20260930.pdf',date='2026-08-31',kind='context',points=0,verified=True,type='Firm Form ADV brochure'),
   dict(title='Acquisition activity',detail='Maridea announced its acquisition of Pultro Financial Management in September 2026.',url='https://marideawealth.com/press/maridea-wealth-management-acquires-pultro-financial-management/',date='2026-09-01',kind='positive',points=10,verified=True,type='Company announcement'),
  ]),
 'Dynasty Financial Partners':dict(
  unknowns=['Whether Equi would complement the Allocate partnership rather than duplicate it','Who owns platform approval and whether an additional provider can be onboarded'],
  analyst='Large distribution potential, but the preferred Allocate relationship creates a substantial competitive barrier.',
  stage='Competitive barrier',
  evidence=[dict(title='Preferred white-label private-markets partner',detail='Allocate and Dynasty announced Allocate as a preferred partner for white-label private market solutions across Dynasty’s advisor network.',url='https://www.allocate.co/news/allocate-and-dynasty-financial-partners-expand-partnership-to-power-private-market-access-and-solutions-business-wire',date='2026-06-10',kind='negative',points=27,verified=True,type='Provider announcement')]),
 'Gresham Partners':dict(
  unknowns=['Current openness to additional external managers','Specific manager-selection gaps and decision cycle'],
  analyst='Uses third-party managers but already structures client-only private partnerships. Pursue a specialist institutional-manager angle, if at all.',
  stage='Research priority',
  evidence=[
   dict(title='Third-party managers selected for client partnerships',detail='Form CRS describes private partnerships with assets managed by managers not affiliated with Gresham.',url='https://reports.adviserinfo.sec.gov/crs/crs_108668.pdf',date='2025-03-31',kind='positive',points=21,verified=True,type='SEC-hosted Form CRS'),
   dict(title='Existing Gresham-advised partnership structures',detail='The same Form CRS describes Gresham-advised private partnerships offered only to its clients, reducing the appeal of a generic replacement product.',url='https://reports.adviserinfo.sec.gov/crs/crs_108668.pdf',date='2025-03-31',kind='negative',points=15,verified=True,type='SEC-hosted Form CRS')]),
 'Bartlett Wealth Management':dict(
  unknowns=['Whether Focus controls preferred-provider and manager-platform decisions','Whether Bartlett currently has unmet private-credit or hedge-fund needs'],
  analyst='Apollo reports an external-manager research function, but that claim and buyer authority need source verification. Parent-level purchasing may matter.',
  stage='Needs verification',
  evidence=[
   dict(title='Part of Focus Financial network',detail='Focus lists Bartlett Wealth Management among its wealth management firms.',url='https://corporate.focuspartners.com/locations/bartlett-wealth-management',date='',kind='negative',points=12,verified=True,type='Parent company directory'),
   dict(title='External-manager research function (Apollo report)',detail='Apollo deep-dive reported a Director of External Manager Research. Public role and decision authority not independently verified.',url='',date='2026-11-23',kind='positive',points=14,verified=False,type='Apollo deep-dive note')]),
 'Ellevest':dict(
  unknowns=['Whether private-investment menu has any gaps','Current vendor relationships and fund approval process'],
  analyst='Apollo inferred no alternatives offering; Ellevest’s own current site contradicts that. Treat as low-priority until a differentiated use case is found.',
  stage='Deprioritized',
  evidence=[
   dict(title='Private investments already offered',detail='Ellevest describes access to private alternative investments through its wealth management services.',url='https://www.ellevest.com/wealth-management',date='',kind='negative',points=10,verified=True,type='Company product page'),
   dict(title='Envestnet invested in Ellevest',detail='Industry coverage confirms Envestnet took a stake, but this alone does not establish a conflicting product partnership.',url='https://www.wealthmanagement.com/wealth-management-industry-trends/envestnet-takes-stake-in-sallie-krawcheck-s-ellevest',date='2022-04-01',kind='context',points=0,verified=True,type='Industry publication')]),
 'FFT Wealth Management':dict(unknowns=['Current parent-level alternatives platform permissions'],analyst='Apollo flagged parent platform complications. Verify before considering outreach.',stage='Needs verification'),
 'Legacy Knight':dict(unknowns=['Whether own principal-investing activities preclude platform partnerships'],analyst='Apollo suggested potential internal build; claim needs sourcing.',stage='Needs verification'),
 'Kovitz':dict(unknowns=['Is this a manager buyer or fund manufacturer?'],analyst='Business model unclear; avoid assuming existing alternatives activity indicates buyer intent.',stage='Needs verification'),
 'Galleon Wealth Management':dict(unknowns=['Apollo reports US headquarters, but description and .co.uk domain indicate a UK firm.'],analyst='Likely location/identity mismatch. Check entity identity before prospecting.',stage='Data quality issue'),
}
accounts=[]
for r in rows:
 name=r['Company Name'];p=P.get(name,{})
 score=int(r[SCORE] or 0)
 # Avoid exporting owner email, phone numbers, addresses, or unneeded PII in public prototype.
 site=r['Website'].strip()
 domain=re.sub(r'^https?://','',site).split('/')[0].removeprefix('www.')
 accounts.append({
  'id':r['Apollo Account Id'] or r['Apollo Org Id'],
  'name':name,
  'domain':domain,
  'website':site,
  'city':r['Company City'],
  'state':r['Company State'],
  'country':r['Company Country'],
  'employees':int(r['# Employees']) if r['# Employees'].isdigit() else None,
  'industry':r['Industry'],
  'fit':score,
  'description':r['Short Description'][:420],
  'parent':r['Ultimate Parent Company Name'] or r['Parent company (Apollo data)'] or r['Apollo Parent Org Name'],
  'stage':p.get('stage','Needs verification'),
  'confidence':'Review verified evidence' if p.get('evidence') else 'Low',
  'unknowns':p.get('unknowns',['Evidence-backed buying signal not yet checked','Current manager/vendor relationships not assessed']),
  'analyst':p.get('analyst','Apollo ICP fit score only. There is not enough verified information to infer buying intent.'),
  'evidence':p.get('evidence',[]),
  'buyerRole':'Head of Alternatives / CIO',
  'buyerName':'',
  'note':'',
  'reviewed':False
 })
(root/'accounts.json').write_text(json.dumps(accounts,indent=2,ensure_ascii=False),encoding='utf-8')
(root/'data.js').write_text('window.SEED_ACCOUNTS='+json.dumps(accounts,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')+';\n',encoding='utf-8')
print('WROTE',len(accounts),'accounts','5 public-source annotated',sum(len(a['evidence']) for a in accounts),'evidence entries')

import { catalog } from './catalog.js';

const statuses = {
  verified: { label: 'Verified', help: 'Reproducible evidence exists for the stated scope.' },
  partial: { label: 'Partial', help: 'Some behavior exists, but coverage or evidence is incomplete.' },
  open: { label: 'Open', help: 'The capability is needed but not yet implemented or verified.' },
  unassessed: { label: 'Unassessed', help: 'The capability is cataloged, but its exact gap has not been inventoried.' },
};

const scopes = {
  parity: { label: 'TypeRB parity', eyebrow: 'LANGUAGE PARITY', description: 'Run the same language and package semantics.' },
  production: { label: 'Production apps', eyebrow: 'APPLICATION READY', description: 'Build and operate a representative full-stack service.' },
  ecosystem: { label: 'Typical ecosystem', eyebrow: 'LANGUAGE LANDSCAPE', description: 'Cover capabilities normally expected from a language platform.' },
};

const state = { query: '', status: 'all', scope: 'all' };
const allItems = catalog.areas.flatMap((area) => area.items);

const element = (name, className, text) => {
  const node = document.createElement(name);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};

const button = (label, active, onClick, className = 'filter-button') => {
  const node = element('button', className, label);
  node.type = 'button';
  node.setAttribute('aria-pressed', String(active));
  node.addEventListener('click', onClick);
  return node;
};

const renderSummary = () => {
  const verified = allItems.filter((item) => item.status === 'verified').length;
  const partial = allItems.filter((item) => item.status === 'partial').length;
  const unassessed = allItems.filter((item) => item.status === 'unassessed').length;
  const values = [
    ['Catalog', allItems.length, `${catalog.areas.length} areas`, 'total'],
    ['Verified', verified, 'Public evidence', 'verified'],
    ['Partial', partial, 'Coverage remains', 'partial'],
    ['Unassessed', unassessed, 'Inventory needed', 'unassessed'],
  ];
  const target = document.querySelector('#summary');
  target.replaceChildren(...values.map(([label, value, note, kind]) => {
    const card = element('article', `summary-card summary-${kind}`);
    card.append(element('span', '', label), element('strong', '', value), element('small', '', note));
    return card;
  }));
};

const renderScopeFilters = () => {
  const target = document.querySelector('#scope-filters');
  target.replaceChildren(...Object.entries(scopes).map(([id, meta]) => {
    const members = allItems.filter((item) => item.scopes.includes(id));
    const verified = members.filter((item) => item.status === 'verified').length;
    const card = button('', state.scope === id, () => {
      state.scope = state.scope === id ? 'all' : id;
      render();
    }, 'scope-card');
    card.append(
      element('span', 'eyebrow', meta.eyebrow),
      (() => {
        const title = element('span', 'scope-title');
        title.append(element('strong', '', meta.label), element('b', '', `${verified} / ${members.length}`));
        return title;
      })(),
      element('span', 'scope-description', meta.description),
      (() => {
        const track = element('span', 'progress-track');
        const fill = element('span');
        fill.style.width = `${Math.round((verified / members.length) * 100)}%`;
        track.append(fill);
        return track;
      })(),
    );
    return card;
  }));
};

const renderStatusFilters = () => {
  const target = document.querySelector('#status-filters');
  const caption = element('span', 'filter-caption', 'STATUS');
  const options = [['all', 'All'], ...Object.entries(statuses).map(([id, meta]) => [id, meta.label])];
  target.replaceChildren(caption, ...options.map(([id, label]) => button(label, state.status === id, () => {
    state.status = id;
    render();
  })));
};

const matches = (area, item) => {
  const query = state.query.trim().toLocaleLowerCase('en');
  const searchable = `${area.title} ${area.description} ${item.title} ${item.description}`.toLocaleLowerCase('en');
  return (state.scope === 'all' || item.scopes.includes(state.scope))
    && (state.status === 'all' || item.status === state.status)
    && (!query || searchable.includes(query));
};

const renderCapability = (item) => {
  const details = element('details', `capability-row status-${item.status}`);
  const summary = element('summary');
  summary.append(
    element('span', 'status-icon', item.status === 'verified' ? '✓' : item.status === 'partial' ? '◌' : '○'),
    element('span', 'capability-title', item.title),
  );
  if (item.evidence) {
    const evidence = element('a', 'evidence-label', item.evidence.label);
    evidence.href = item.evidence.url;
    evidence.target = '_blank';
    evidence.rel = 'noreferrer';
    evidence.addEventListener('click', (event) => event.stopPropagation());
    summary.append(evidence);
  } else {
    summary.append(element('span'));
  }
  summary.append(element('span', 'status-label', statuses[item.status].label), element('span', 'detail-chevron', '⌄'));

  const body = element('div', 'capability-detail');
  body.append(element('p', '', item.description));
  const meta = element('div', 'detail-meta');
  meta.append(element('span', '', statuses[item.status].help));
  const lenses = element('span', 'scope-list');
  item.scopes.forEach((scope) => lenses.append(element('span', 'scope-badge', scopes[scope].label)));
  meta.append(lenses);
  body.append(meta);
  details.append(summary, body);
  return details;
};

const renderAreas = () => {
  const target = document.querySelector('#area-list');
  let visible = 0;
  const areaNodes = catalog.areas.flatMap((area) => {
    const items = area.items.filter((item) => matches(area, item));
    if (items.length === 0) return [];
    visible += items.length;
    const verified = items.filter((item) => item.status === 'verified').length;
    const details = element('details', 'area-card');
    details.open = true;
    const summary = element('summary', 'area-summary');
    summary.append(
      element('span', 'area-icon', verified === items.length ? '✓' : verified),
      (() => {
        const heading = element('span', 'area-heading');
        heading.append(element('strong', '', area.title), element('small', '', area.description));
        return heading;
      })(),
      element('span', 'area-meta', `${verified} / ${items.length} verified`),
      element('span', 'area-chevron', '⌄'),
    );
    const list = element('div', 'capability-list');
    list.append(...items.map(renderCapability));
    details.append(summary, list);
    return [details];
  });
  if (areaNodes.length === 0) {
    const empty = element('div', 'empty-state');
    empty.append(element('strong', '', 'No matching capabilities'), element('span', '', 'Change the search or filters.'));
    areaNodes.push(empty);
  }
  target.replaceChildren(...areaNodes);
  document.querySelector('#visible-count').textContent = `${visible} shown`;
};

const render = () => {
  renderScopeFilters();
  renderStatusFilters();
  renderAreas();
};

document.querySelector('#snapshot-date').textContent = `Catalog snapshot · ${catalog.updatedAt}`;
document.querySelector('#search').addEventListener('input', (event) => {
  state.query = event.target.value;
  renderAreas();
});
document.querySelector('#expand-all').addEventListener('click', () => {
  document.querySelectorAll('#area-list details').forEach((node) => { node.open = true; });
});
document.querySelector('#collapse-all').addEventListener('click', () => {
  document.querySelectorAll('#area-list details').forEach((node) => { node.open = false; });
});

renderSummary();
render();

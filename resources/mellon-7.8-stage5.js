/* Exact H3 signs on native Cartofreako anchors. Null support stays unavailable. */
const signed = x => (x > 0 ? '+' : '') + (Math.abs(x) > 0 && Math.abs(x) < .0005 ? x.toPrecision(6) : x.toFixed(3));
for (const root of document.querySelectorAll('.gojira-h3')) {
  (async () => {
    const response = await fetch(root.dataset.source);
    if (!response.ok) throw Error('Map data unavailable');
    const data = await response.json(), features = new Map(data.features.map(f => [f.properties.h3, f.properties]));
    const role = root.querySelector('[data-role]'), mode = root.querySelector('[data-mode]'), coverage = root.querySelector('[data-coverage]');
    const status = root.querySelector('[data-status]'), detail = root.querySelector('[data-detail]'), tbody = root.querySelector('tbody');
    const update = () => {
      const stem = role.value + '_' + mode.value;
      let hot = 0, cold = 0, unavailable = 0;
      tbody.replaceChildren();
      for (const circle of root.querySelectorAll('.h3-point')) {
        const p = features.get(circle.dataset.cell), delta = p[stem + '_delta_pp'];
        const missing = delta === null, zero = delta === 0;
        circle.style.display = missing ? (coverage.checked ? '' : 'none') : zero ? 'none' : '';
        circle.setAttribute('fill', missing ? 'none' : delta > 0 ? '#d62728' : '#1565c0');
        circle.setAttribute('stroke', missing ? '#666' : 'white');
        circle.setAttribute('tabindex', circle.style.display === 'none' ? '-1' : '0');
        if (missing) unavailable++; else if (delta > 0) hot++; else if (delta < 0) cold++;
        const values = missing ? ['Unavailable', 'Unavailable', 'Unavailable'] : [p[stem + '_left_share'].toPrecision(6) + '%', p[stem + '_right_share'].toPrecision(6) + '%', signed(delta)];
        const sign = missing ? 'Unavailable' : zero ? 'Equal' : delta > 0 ? 'Hot' : 'Cold';
        const tip = `${sign}: H3 ${p.h3}; Minus One ${values[0]}; The New Empire ${values[1]}; difference ${values[2]} pp; ${role.value}, ${mode.value}; weeks ${data.metadata.weeks.join(', ')}; common observations ${p.common_intervals} of ${p.expected_intervals}.`;
        circle.setAttribute('aria-label', tip);circle.dataset.tooltip = tip;circle.querySelector('title').textContent = tip;
        if (!missing || coverage.checked) {
          const tr = document.createElement('tr');
          for (const value of [p.h3, sign, ...values, `${p.common_intervals} of ${p.expected_intervals}`]) { const td = document.createElement('td'); td.textContent = value; tr.append(td); }
          tbody.append(tr);
        }
      }
      status.textContent = `${hot} hot, ${cold} cold; ${unavailable} unavailable cells. Circle centers are display anchors, not precise audience locations.`;
      detail.textContent = 'Focus or hover a circle for its exact shares, period and coverage.';
    };
    for (const circle of root.querySelectorAll('.h3-point')) {
      const describe = () => { detail.textContent = circle.dataset.tooltip; };
      circle.addEventListener('focus', describe);
      circle.addEventListener('pointerenter', describe);
    }
    for (const input of [role, mode, coverage]) input.addEventListener('change', update);
    update();root.dataset.ready = 'true';
  })().catch(error => {root.querySelector('[data-status]').textContent = error.message;});
}

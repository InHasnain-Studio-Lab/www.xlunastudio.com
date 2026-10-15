// XLUNA particle universe. Every page opens on the XLUNA title, which then folds into tonight's real moon
// circled by two crossing orbits; scrolling carries the particles out into a galaxy.
(function () {
  const SYNODIC = 29.530588853;
  const REF_NEW_MOON = Date.UTC(2000, 0, 6, 18, 14);
  const PHASES = [[1.84, "New moon"], [5.53, "Waxing crescent"], [9.22, "First quarter"], [12.91, "Waxing gibbous"],
    [16.61, "Full moon"], [20.3, "Waning gibbous"], [23.99, "Last quarter"], [27.68, "Waning crescent"], [99, "New moon"]];
  const age = (((Date.now() - REF_NEW_MOON) / 864e5) % SYNODIC + SYNODIC) % SYNODIC;
  const elong = age / SYNODIC * Math.PI * 2;
  const lit = (1 - Math.cos(elong)) / 2;
  const phaseName = PHASES.find(p => age < p[0])[1];
  document.querySelectorAll("[data-moon-phase]").forEach(el => {
    el.textContent = `Tonight's moon · ${phaseName} · ${Math.round(lit * 100)}% lit · day ${age.toFixed(1)} of ${SYNODIC.toFixed(1)}`;
  });

  const canvas = document.getElementById("universe");
  if (!canvas || !window.THREE) return;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const small = innerWidth < 760;
  const N = small ? 8000 : 17000;
  const order = ["dust", "word", "moonOrbit", "galaxy"];
  const INTRO_STEPS = 2;
  const HOLD = [0, 1.7];
  const MORPH = 2.3;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.setClearColor(0x04060c, 1);
  const world = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 120);

  const rnd = (a, b) => a + Math.random() * (b - a);
  const WHITE = [0.93, 0.95, 0.98], ICE = [0.56, 0.9, 1.0], AMBER = [1.0, 0.69, 0.29];

  // Near-side lunar features in selenographic degrees: lat, lon, lat radius, lon radius, darkness.
  const MARIA = [[10, -56, 30, 21, .55], [33, -16, 16, 18, .62], [28, 17, 10, 11, .6], [8, 30, 11, 13, .6], [17, 59, 7, 9, .62],
    [-7, 51, 10, 8, .55], [-15, 35, 6, 6, .55], [-21, -17, 11, 12, .5], [-24, -39, 6, 6, .55], [56, 0, 5, 38, .45],
    [13, 4, 4, 5, .5], [-10, -23, 5, 5, .45], [7, -31, 7, 8, .45]];
  const CRATERS = [[-43, -11, 3.2, .9], [9.6, -20, 3, .55], [8, -38, 1.6, .5], [23.7, -47.4, 1.3, 1]];
  function albedo(la, lo) {
    let a = 0.8;
    for (const [mla, mlo, rla, rlo, dark] of MARIA) {
      const d = ((la - mla) / rla) ** 2 + ((lo - mlo) / rlo) ** 2;
      a -= dark * 0.6 * Math.pow(Math.max(0, Math.min(1, 1.2 - d)), 1.4);
    }
    for (const [cla, clo, r, glow] of CRATERS) {
      const d = Math.hypot(la - cla, (lo - clo) * Math.cos(cla * Math.PI / 180));
      a += glow * 0.4 * Math.exp(-((d / r) ** 2));
    }
    // Tycho's ray system across the southern highlands.
    const ang = Math.atan2(la + 43, (lo + 11) * 0.73), dist = Math.hypot(la + 43, lo + 11);
    a += 0.14 * Math.min(1, Math.pow(Math.cos(ang * 9 + .7), 40) + Math.pow(Math.cos(ang * 13 + 2.1), 60)) * Math.exp(-dist / 45);
    return Math.max(0.12, Math.min(1, a * (0.9 + Math.random() * 0.2)));
  }

  function dust() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      p[i*3] = rnd(-14, 14); p[i*3+1] = rnd(-9, 9); p[i*3+2] = rnd(-10, 4);
      const b = rnd(0.04, 0.16); for (let k = 0; k < 3; k++) c[i*3+k] = WHITE[k] * b;
    }
    return { p, c };
  }

  // The XLUNA title, traced from the same strokes as the logo wordmark.
  function word() {
    const W = 1100, H = 240, cv = document.createElement("canvas");
    cv.width = W; cv.height = H;
    const g = cv.getContext("2d");
    g.translate(30, 40); g.scale(2, 1.6);
    g.lineWidth = 11; g.lineCap = "square"; g.lineJoin = "miter"; g.miterLimit = 1.5; g.strokeStyle = "#fff";
    ["M0 0 L80 100 M80 0 L0 100", "M112 0 V100 H180", "M212 0 V58 A40 40 0 0 0 292 58 V0", "M324 100 V0 L404 100 V0", "M436 100 L476 0 L516 100"]
      .forEach(d => g.stroke(new Path2D(d)));
    const data = g.getImageData(0, 0, W, H).data, pts = [];
    for (let y = 0; y < H; y += 2) for (let x = 0; x < W; x += 2) if (data[(y * W + x) * 4 + 3] > 140) pts.push(x, y);
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    const span = small ? 7.2 : 10.5, sc = span / W, count = pts.length / 2;
    for (let i = 0; i < N; i++) {
      const j = (Math.random() * count | 0) * 2, x = pts[j], y = pts[j + 1];
      p[i*3] = (x - W / 2) * sc + rnd(-0.02, 0.02); p[i*3+1] = -(y - H / 2) * sc + rnd(-0.02, 0.02); p[i*3+2] = rnd(-0.15, 0.15);
      const col = x < 214 ? ICE : WHITE, b = rnd(0.6, 1);
      for (let k = 0; k < 3; k++) c[i*3+k] = col[k] * b;
    }
    return { p, c };
  }

  // Tonight's moon, lit from the sun's real direction, plus two orbits crossing in front of it like the logo.
  const MOON_R = small ? 1.45 : 1.75, RING_R = MOON_R * 1.95, RING_SHARE = 0.36;
  const ringStart = Math.floor(N * (1 - RING_SHARE));
  const ringA0 = new Float32Array(N), ringId = new Uint8Array(N), ringJit = new Float32Array(N);
  function moonOrbit() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    const L = new THREE.Vector3(Math.sin(elong), 0.12, -Math.cos(elong)).normalize();
    for (let i = 0; i < ringStart; i++) {
      let nx, ny, nz;
      do {
        const u = Math.random() * 2 - 1, t = Math.random() * Math.PI * 2, s = Math.sqrt(1 - u * u);
        nx = s * Math.cos(t); ny = u; nz = s * Math.sin(t);
      } while (nz < -0.1);
      const la = Math.asin(ny) * 180 / Math.PI, lo = Math.atan2(nx, nz) * 180 / Math.PI;
      const alb = albedo(la, lo);
      const lam = Math.max(0, nx * L.x + ny * L.y + nz * L.z);
      const light = Math.pow(Math.min(1, lam * 1.6), 0.75);
      const earthshine = 0.1 * (1 - light);
      p[i*3] = nx * MOON_R; p[i*3+1] = ny * MOON_R; p[i*3+2] = nz * MOON_R;
      const v = alb * (light * 1.15 + earthshine);
      const rim = light * Math.pow(1 - nz, 2) * 0.25;
      c[i*3] = v * 0.96; c[i*3+1] = v * 0.99 + rim * 0.6; c[i*3+2] = v * 1.05 + rim + (1 - light) * 0.03;
    }
    for (let i = ringStart; i < N; i++) {
      ringId[i] = i & 1; ringA0[i] = Math.random() * Math.PI * 2; ringJit[i] = rnd(-0.03, 0.03);
    }
    placeRings(p, c, 0);
    return { p, c };
  }
  // TILT opens each ring from edge-on to the same thin ellipse as the logo (minor/major about 0.22).
  const TILT = 0.24, ROLL = 34 * Math.PI / 180;
  function placeRings(p, c, time) {
    const cz = Math.cos(TILT), sz = Math.sin(TILT);
    for (let i = ringStart; i < N; i++) {
      const a = ringA0[i] + time * 0.35, r = RING_R + ringJit[i];
      const x = Math.cos(a) * r, z = Math.sin(a) * r;
      const y2 = -z * sz, z2 = z * cz;
      const roll = ringId[i] ? ROLL : -ROLL, cr = Math.cos(roll), sr = Math.sin(roll);
      const x3 = x * cr - y2 * sr, y3 = x * sr + y2 * cr;
      p[i*3] = x3; p[i*3+1] = y3; p[i*3+2] = z2;
      // Ring particles passing behind the moon disc are hidden so the moon reads as solid.
      const hidden = z2 < 0 && Math.hypot(x3, y3) < MOON_R * 0.98;
      const b = hidden ? 0 : z2 > 0 ? 1 : 0.45;
      const t = (Math.sin(a * 2) + 1) / 2;
      c[i*3] = (WHITE[0] * t + ICE[0] * (1 - t)) * b; c[i*3+1] = (WHITE[1] * t + ICE[1] * (1 - t)) * b; c[i*3+2] = b;
    }
  }

  function galaxy() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const arm = i % 2, d = Math.pow(Math.random(), 0.7) * 7, ang = d * 0.85 + arm * Math.PI + rnd(-0.4, 0.4);
      p[i*3] = Math.cos(ang) * d; p[i*3+1] = rnd(-0.2, 0.2) * (1.3 - d / 7); p[i*3+2] = Math.sin(ang) * d;
      const col = Math.random() < 0.04 ? AMBER : Math.random() < 0.3 ? ICE : WHITE, b = rnd(0.4, 1) * (1.15 - d / 9);
      for (let q = 0; q < 3; q++) c[i*3+q] = col[q] * b;
    }
    return { p, c };
  }

  const BUILD = { dust, word, moonOrbit, galaxy };
  const states = order.map(n => BUILD[n]());
  const POSE = { dust: { spin: 0.02, tilt: 0, cam: 11 }, word: { spin: 0, tilt: 0, cam: small ? 10 : 9 },
    moonOrbit: { spin: 0, tilt: 0, cam: 9.5 }, galaxy: { spin: 0.05, tilt: 0.55, cam: 11 } };
  // Hero copy sits in the lower half, so formations rise into the space above it.
  const LIFT = document.body.dataset.scene === "home" ? 1.7 : 1.25;

  const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
  pos.set(states[0].p); col.set(states[0].c);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const dot = document.createElement("canvas"); dot.width = dot.height = 64;
  const dg = dot.getContext("2d"), grd = dg.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)"); grd.addColorStop(0.35, "rgba(255,255,255,0.4)"); grd.addColorStop(1, "rgba(255,255,255,0)");
  dg.fillStyle = grd; dg.fillRect(0, 0, 64, 64);
  const mat = new THREE.PointsMaterial({ size: small ? 0.085 : 0.072, map: new THREE.CanvasTexture(dot), vertexColors: true,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  mat.color.setScalar(2.6);
  const cloud = new THREE.Points(geo, mat);
  world.add(cloud);

  const sg = new THREE.BufferGeometry(), sp = new Float32Array(1800 * 3);
  for (let i = 0; i < sp.length; i += 3) { sp[i] = rnd(-50, 50); sp[i+1] = rnd(-30, 30); sp[i+2] = rnd(-50, -12); }
  sg.setAttribute("position", new THREE.BufferAttribute(sp, 3));
  world.add(new THREE.Points(sg, new THREE.PointsMaterial({ size: 0.07, color: 0x6f7a8e, transparent: true, opacity: 0.8, depthWrite: false })));

  camera.position.z = POSE.dust.cam;
  function resize() {
    renderer.setSize(innerWidth, innerHeight, false);
    camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
  }
  addEventListener("resize", resize); resize();

  let mx = 0, my = 0;
  addEventListener("pointermove", e => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; });

  const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  function introAt(sec) {
    let tt = sec;
    for (let step = 0; step < INTRO_STEPS; step++) {
      tt -= HOLD[step];
      if (tt < MORPH) return step + Math.max(0, tt) / MORPH;
      tt -= MORPH;
    }
    return INTRO_STEPS;
  }
  const t0 = performance.now();
  let k = reduce ? INTRO_STEPS : 0, last = t0, spin = 0;
  const moonState = states[2];

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const scrollK = Math.min(1, (scrollY / max) * 1.6);
    const target = (reduce ? INTRO_STEPS : introAt((now - t0) / 1000)) + scrollK;
    k += (target - k) * Math.min(1, dt * 5);
    if (!reduce) placeRings(moonState.p, moonState.c, (now - t0) / 1000);

    const i = Math.min(states.length - 1, Math.floor(k)), j = Math.min(states.length - 1, i + 1), f = ease(k - i);
    const A = states[i], B = states[j];
    for (let q = 0; q < N * 3; q++) {
      pos[q] = A.p[q] + (B.p[q] - A.p[q]) * f;
      col[q] = A.c[q] + (B.c[q] - A.c[q]) * f;
    }
    geo.attributes.position.needsUpdate = true;
    geo.attributes.color.needsUpdate = true;

    const pa = POSE[order[i]], pb = POSE[order[j]];
    const spinRate = pa.spin + (pb.spin - pa.spin) * f, tilt = pa.tilt + (pb.tilt - pa.tilt) * f;
    // The title and the moon face the viewer, so any spin unwinds before they settle.
    spin = spinRate > 0.001 ? spin + dt * spinRate * 6 : spin * (1 - Math.min(1, dt * 2.5));
    cloud.rotation.y = spin + mx * 0.18;
    cloud.rotation.x += ((tilt + my * 0.12) - cloud.rotation.x) * 0.05;
    camera.position.z += ((pa.cam + (pb.cam - pa.cam) * f) - camera.position.z) * 0.05;
    const lift = Math.max(0, 1 - scrollY / innerHeight) * LIFT;
    cloud.position.y += (lift - cloud.position.y) * 0.08;
    renderer.render(world, camera);
    if (!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

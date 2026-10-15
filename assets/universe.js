// XLUNA particle universe. Every page opens on the XLUNA title, which then folds into the XLUNA mark
// (a thin new-moon crescent crossed by a beam of light); scrolling carries the particles out into a galaxy.
(function () {
  const SYNODIC = 29.530588853;
  const REF_NEW_MOON = Date.UTC(2000, 0, 6, 18, 14);
  const PHASES = [[1.84, "New moon"], [5.53, "Waxing crescent"], [9.22, "First quarter"], [12.91, "Waxing gibbous"],
    [16.61, "Full moon"], [20.3, "Waning gibbous"], [23.99, "Last quarter"], [27.68, "Waning crescent"], [99, "New moon"]];
  const age = (((Date.now() - REF_NEW_MOON) / 864e5) % SYNODIC + SYNODIC) % SYNODIC;
  const lit = (1 - Math.cos(age / SYNODIC * Math.PI * 2)) / 2;
  const phaseName = PHASES.find(p => age < p[0])[1];
  document.querySelectorAll("[data-moon-phase]").forEach(el => {
    el.textContent = `Tonight's moon · ${phaseName} · ${Math.round(lit * 100)}% lit · day ${age.toFixed(1)} of ${SYNODIC.toFixed(1)}`;
  });

  const canvas = document.getElementById("universe");
  if (!canvas || !window.THREE) return;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const small = innerWidth < 760;
  const N = small ? 8000 : 17000;
  const order = ["dust", "word", "mark", "galaxy"];
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
  const BEAM_HI = [0.84, 0.96, 1.0], BEAM_LO = [0.36, 0.78, 0.94];

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

  // The XLUNA mark, in the logo's own 120-unit coordinates: crescent = circle (60,60) r52 minus circle (67,53) r50.5;
  // the beam runs from (118,2) to (2,118) and stops short of the crescent, as the logo's gap mask does.
  const UNIT = (small ? 1.55 : 1.9) / 52;
  const toWorld = (x, y) => [(x - 60) * UNIT, (60 - y) * UNIT];
  const inCrescent = (x, y, ro, ri) => Math.hypot(x - 60, y - 60) < ro && Math.hypot(x - 67, y - 53) > ri;
  const beamStart = Math.floor(N * 0.7), haloStart = Math.floor(N * 0.58);
  const beamU = new Float32Array(N), beamBase = new Float32Array(N);
  function mark() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    const crescentPt = () => {
      let x, y;
      do { x = rnd(8, 112); y = rnd(8, 112); } while (!inCrescent(x, y, 52, 50.5));
      return [x, y];
    };
    for (let i = 0; i < haloStart; i++) {
      const [x, y] = crescentPt(), [wx, wy] = toWorld(x, y);
      const dome = Math.sqrt(Math.max(0, 52 * 52 - (x - 60) ** 2 - (y - 60) ** 2)) * UNIT * 0.25;
      p[i*3] = wx; p[i*3+1] = wy; p[i*3+2] = dome + rnd(-0.03, 0.03);
      const t = Math.min(1, Math.max(0, (x + y - 40) / 170)), b = rnd(0.75, 1);
      for (let k = 0; k < 3; k++) c[i*3+k] = (WHITE[k] * (1 - t) + ICE[k] * t) * b;
    }
    // A faint glow that hugs the outside of the crescent.
    for (let i = haloStart; i < beamStart; i++) {
      const [x, y] = crescentPt(), ang = Math.atan2(y - 60, x - 60), push = rnd(0.5, 5);
      const [wx, wy] = toWorld(x + Math.cos(ang) * push, y + Math.sin(ang) * push);
      p[i*3] = wx; p[i*3+1] = wy; p[i*3+2] = rnd(-0.1, 0.1);
      const b = rnd(0.08, 0.28) * (1 - push / 6);
      for (let k = 0; k < 3; k++) c[i*3+k] = ICE[k] * b;
    }
    for (let i = beamStart; i < N; i++) {
      let u, x, y;
      do {
        u = Math.random();
        const width = 4.4 * Math.pow(1 - Math.abs(2 * u - 1), 1.1), off = rnd(-0.5, 0.5) * width;
        x = 118 - 116 * u + off * 0.7071; y = 2 + 116 * u + off * 0.7071;
      } while (inCrescent(x, y, 56, 46));
      const [wx, wy] = toWorld(x, y);
      p[i*3] = wx; p[i*3+1] = wy; p[i*3+2] = rnd(-0.04, 0.04) + 0.08;
      beamU[i] = u; beamBase[i] = rnd(0.55, 1);
    }
    shineBeam(c, 0);
    return { p, c };
  }
  // Light travels down the beam from the top-right, like the logo's glow catching the blade.
  function shineBeam(c, time) {
    const head = (time * 0.32) % 1.4 - 0.2;
    for (let i = beamStart; i < N; i++) {
      const u = beamU[i], pulse = Math.exp(-((u - head) ** 2) / 0.006);
      const b = beamBase[i] * (0.55 + 0.9 * pulse);
      for (let k = 0; k < 3; k++) c[i*3+k] = (BEAM_HI[k] * (1 - u) + BEAM_LO[k] * u) * b;
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

  const BUILD = { dust, word, mark, galaxy };
  const states = order.map(n => BUILD[n]());
  const POSE = { dust: { spin: 0.02, tilt: 0, cam: 11 }, word: { spin: 0, tilt: 0, cam: small ? 10 : 9 },
    mark: { spin: 0, tilt: 0, cam: 9.5 }, galaxy: { spin: 0.05, tilt: 0.55, cam: 11 } };
  // Hero copy sits in the lower half, so formations rise into the space above it.
  const LIFT = document.body.dataset.scene === "home" ? 1.7 : 1.25;

  const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
  pos.set(states[0].p); col.set(states[0].c);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const dot = document.createElement("canvas"); dot.width = dot.height = 64;
  const dg = dot.getContext("2d"), grd = dg.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)"); grd.addColorStop(0.45, "rgba(255,255,255,0.85)"); grd.addColorStop(0.7, "rgba(255,255,255,0.3)"); grd.addColorStop(1, "rgba(255,255,255,0)");
  dg.fillStyle = grd; dg.fillRect(0, 0, 64, 64);
  const mat = new THREE.PointsMaterial({ size: small ? 0.09 : 0.078, map: new THREE.CanvasTexture(dot), vertexColors: true,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  mat.color.setScalar(1.5);
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
  const markState = states[2];

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const scrollK = Math.min(1, (scrollY / max) * 1.6);
    const target = (reduce ? INTRO_STEPS : introAt((now - t0) / 1000)) + scrollK;
    k += (target - k) * Math.min(1, dt * 5);
    if (!reduce) shineBeam(markState.c, (now - t0) / 1000);

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
    // The title and the mark face the viewer, so any spin unwinds before they settle.
    spin = spinRate > 0.001 ? spin + dt * spinRate * 6 : spin * (1 - Math.min(1, dt * 2.5));
    cloud.rotation.y = spin + mx * 0.18;
    cloud.rotation.x += ((tilt + my * 0.12) - cloud.rotation.x) * 0.05;
    camera.position.z += ((pa.cam + (pb.cam - pa.cam) * f) - camera.position.z) * 0.05;
    // Past the opening screen the particles become a dim backdrop so body text stays readable.
    canvas.style.opacity = Math.max(0.22, 1 - Math.max(0, scrollY - innerHeight * 0.3) / (innerHeight * 0.6)).toFixed(3);
    const lift = Math.max(0, 1 - scrollY / innerHeight) * LIFT;
    cloud.position.y += (lift - cloud.position.y) * 0.08;
    renderer.render(world, camera);
    if (!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

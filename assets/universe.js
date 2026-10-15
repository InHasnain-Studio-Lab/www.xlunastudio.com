// XLUNA particle universe. Each page names a sequence of formations in <body data-scene>;
// the intro plays them on a timer, then scrolling carries the particles through the rest.
(function () {
  const canvas = document.getElementById("universe");
  if (!canvas || !window.THREE) return;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const small = innerWidth < 760;
  const N = small ? 7000 : 15000;
  const SCENES = {
    home: { intro: ["dust", "moon", "word"], scroll: ["orbits", "galaxy"], hold: [0, 1.8] },
    store: { intro: ["dust", "orbits"], scroll: ["galaxy"], hold: [0] },
    about: { intro: ["dust", "moon"], scroll: ["word", "galaxy"], hold: [0] },
    contact: { intro: ["dust", "moon"], scroll: [], hold: [0] }
  };
  const scene = SCENES[document.body.dataset.scene] || SCENES.home;
  const order = scene.intro.concat(scene.scroll);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.setClearColor(0x04060c, 1);
  const world = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 120);

  const rnd = (a, b) => a + Math.random() * (b - a);
  const WHITE = [0.93, 0.95, 0.98], ICE = [0.56, 0.9, 1.0], AMBER = [1.0, 0.69, 0.29];

  function dust() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      p[i*3] = rnd(-14, 14); p[i*3+1] = rnd(-9, 9); p[i*3+2] = rnd(-10, 4);
      const b = rnd(0.08, 0.3); c[i*3] = WHITE[0]*b; c[i*3+1] = WHITE[1]*b; c[i*3+2] = WHITE[2]*b;
    }
    return { p, c };
  }

  // New moon: the sun sits behind it, so only a thin limb crescent is lit; earthshine keeps the disc faintly visible.
  function moon() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    const L = new THREE.Vector3(0.62, 0.42, -0.66).normalize();
    for (let i = 0; i < N; i++) {
      let nx, ny, nz;
      // A quarter of the particles are placed on the sunlit limb so the crescent reads clearly.
      for (let tries = 0; tries < 40; tries++) {
        const u = Math.random() * 2 - 1, t = Math.random() * Math.PI * 2, s = Math.sqrt(1 - u * u);
        nx = s * Math.cos(t); ny = u; nz = s * Math.sin(t);
        if (i % 4 || (nx * L.x + ny * L.y + nz * L.z > 0.25 && Math.abs(nz) < 0.4)) break;
      }
      const crater = Math.sin(nx * 11) * Math.cos(ny * 9) * 0.035;
      const r = 1.9 + crater;
      p[i*3] = nx * r; p[i*3+1] = ny * r; p[i*3+2] = nz * r;
      const lit = Math.max(0, nx * L.x + ny * L.y + nz * L.z);
      const limb = Math.pow(1 - Math.abs(nz), 2);
      const glow = Math.min(1.4, Math.pow(lit, 0.6) * (0.4 + limb * 2.4));
      const base = 0.035 + Math.random() * 0.045;
      const col = glow > 0.35 ? WHITE : ICE;
      for (let k = 0; k < 3; k++) c[i*3+k] = base + col[k] * glow;
    }
    return { p, c };
  }

  // The XLUNA wordmark, traced from the same strokes as the logo SVG.
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
      p[i*3] = (x - W / 2) * sc + rnd(-0.02, 0.02);
      p[i*3+1] = -(y - H / 2) * sc + rnd(-0.02, 0.02);
      p[i*3+2] = rnd(-0.18, 0.18);
      const isX = x < 30 + 92 * 2, col = isX ? ICE : WHITE, b = rnd(0.55, 1);
      for (let k = 0; k < 3; k++) c[i*3+k] = col[k] * b;
    }
    return { p, c };
  }

  function orbits() {
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const k = i % 8;
      if (k === 7) {
        const u = Math.random() * 2 - 1, t = Math.random() * Math.PI * 2, s = Math.sqrt(1 - u * u), r = 0.75;
        p[i*3] = s * Math.cos(t) * r; p[i*3+1] = u * r; p[i*3+2] = s * Math.sin(t) * r;
        for (let q = 0; q < 3; q++) c[i*3+q] = WHITE[q] * 0.7;
        continue;
      }
      const R = 1.4 + k * 0.6, a = Math.random() * Math.PI * 2, w = rnd(-0.05, 0.05), tilt = 0.4 + k * 0.05;
      const x = Math.cos(a) * (R + w), z = Math.sin(a) * (R + w);
      p[i*3] = x; p[i*3+1] = z * Math.sin(tilt) + rnd(-0.03, 0.03); p[i*3+2] = z * Math.cos(tilt);
      const col = Math.random() < 0.3 ? ICE : WHITE, b = rnd(0.45, 1);
      for (let q = 0; q < 3; q++) c[i*3+q] = col[q] * b;
    }
    return { p, c };
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

  // Hero copy sits in the lower half, so the formation rises into the space above it.
  const LIFT = scene === SCENES.home ? 1.7 : 1.2;
  const BUILD = { dust, moon, word, orbits, galaxy };
  const states = order.map(n => BUILD[n]());
  // Per-formation pose: how much the cloud spins and tilts, and how far the camera sits.
  const POSE = {
    dust: { spin: 0.02, tilt: 0, cam: 11 }, moon: { spin: 0, tilt: 0, cam: 9.5 }, word: { spin: 0, tilt: 0, cam: small ? 10 : 9 },
    orbits: { spin: 0.08, tilt: 0.28, cam: 10 }, galaxy: { spin: 0.05, tilt: 0.55, cam: 11 }
  };

  const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
  pos.set(states[0].p); col.set(states[0].c);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const dot = document.createElement("canvas"); dot.width = dot.height = 64;
  const dg = dot.getContext("2d"), grd = dg.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)"); grd.addColorStop(0.35, "rgba(255,255,255,0.4)"); grd.addColorStop(1, "rgba(255,255,255,0)");
  dg.fillStyle = grd; dg.fillRect(0, 0, 64, 64);
  const mat = new THREE.PointsMaterial({ size: small ? 0.08 : 0.068, map: new THREE.CanvasTexture(dot), vertexColors: true,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  mat.color.setScalar(1.7);
  const cloud = new THREE.Points(geo, mat);
  world.add(cloud);

  const sg = new THREE.BufferGeometry(), sp = new Float32Array(1800 * 3);
  for (let i = 0; i < sp.length; i += 3) { sp[i] = rnd(-50, 50); sp[i+1] = rnd(-30, 30); sp[i+2] = rnd(-50, -12); }
  sg.setAttribute("position", new THREE.BufferAttribute(sp, 3));
  world.add(new THREE.Points(sg, new THREE.PointsMaterial({ size: 0.07, color: 0x6f7a8e, transparent: true, opacity: 0.8, depthWrite: false })));

  camera.position.z = POSE[order[0]].cam;

  function resize() {
    renderer.setSize(innerWidth, innerHeight, false);
    camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
  }
  addEventListener("resize", resize); resize();

  let mx = 0, my = 0;
  addEventListener("pointermove", e => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; });

  const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const MORPH = 2.4;
  const introSteps = scene.intro.length - 1;
  const t0 = performance.now();
  let k = reduce ? introSteps : 0, last = t0, spin = 0;

  function introAt(sec) {
    let tt = sec, step = 0;
    for (; step < introSteps; step++) {
      tt -= scene.hold[step] || 0;
      if (tt < MORPH) return step + Math.max(0, tt) / MORPH;
      tt -= MORPH;
    }
    return introSteps;
  }

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const scrollK = scene.scroll.length ? Math.min(scene.scroll.length, (scrollY / max) * (scene.scroll.length + 0.4)) : 0;
    const target = (reduce ? introSteps : introAt((now - t0) / 1000)) + scrollK;
    k += (target - k) * Math.min(1, dt * 5);

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
    // Formations that face the viewer (moon, word) unwind any spin so the crescent and letters read correctly.
    spin = spinRate > 0.001 ? spin + dt * spinRate * 6 : spin * (1 - Math.min(1, dt * 2.5));
    cloud.rotation.y = spin + mx * 0.35;
    cloud.rotation.x += ((tilt + my * 0.25) - cloud.rotation.x) * 0.05;
    camera.position.z += ((pa.cam + (pb.cam - pa.cam) * f) - camera.position.z) * 0.05;
    const lift = Math.max(0, 1 - scrollY / innerHeight) * LIFT;
    cloud.position.y += (lift - cloud.position.y) * 0.08;
    renderer.render(world, camera);
    if (!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

import { motion, AnimatePresence, useInView, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'
import './index.css'

// ─── Shared animation config ───────────────────────────────────────────────
const spring = { type: 'spring', stiffness: 100, damping: 20 }

const wordVariant = {
  hidden:  { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: spring },
}
const staggerWords = {
  hidden:  {},
  visible: { transition: { staggerChildren: 0.1 } },
}
const slideDown = {
  hidden:  { opacity: 0, y: -24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } },
}

// ─── Navbar ────────────────────────────────────────────────────────────────
function Navbar() {
  return (
    <motion.nav
      variants={slideDown}
      initial="hidden"
      animate="visible"
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
        padding: '16px 48px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        background: 'rgba(6,8,16,0.88)',
        backdropFilter: 'blur(24px)',
        borderBottom: '1px solid rgba(0,255,136,0.07)',
      }}
    >
      <span className="font-syne" style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '0.06em', color: '#00ff88' }}>
        MANCHESTER HOMES
      </span>
      <div className="nav-links" style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
        {['Features', 'Dashboard'].map(item => (
          <span
            key={item}
            className="font-grotesk"
            style={{ fontSize: '13px', fontWeight: 500, letterSpacing: '0.12em', color: 'rgba(255,255,255,0.4)', cursor: 'pointer', textTransform: 'uppercase', transition: 'color 0.2s ease' }}
            onMouseEnter={e => (e.target.style.color = '#00ff88')}
            onMouseLeave={e => (e.target.style.color = 'rgba(255,255,255,0.4)')}
          >{item}</span>
        ))}
        <motion.a
          href="https://manchester-homes.streamlit.app"
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.97 }}
          transition={spring}
          style={{ padding: '8px 22px', background: '#00ff88', borderRadius: '7px', color: '#060810', fontSize: '13px', fontWeight: 700, letterSpacing: '0.08em', textDecoration: 'none', fontFamily: 'Syne, sans-serif' }}
        >
          LAUNCH APP
        </motion.a>
      </div>
    </motion.nav>
  )
}

// ─── Hero ──────────────────────────────────────────────────────────────────
function Hero() {
  return (
    <section
      className="hero-section"
      style={{
        position: 'relative', minHeight: '100vh',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        padding: '140px 48px 80px', textAlign: 'center', overflow: 'hidden',
      }}
    >
      <div className="hero-grid" />
      <div style={{
        position: 'absolute', top: '38%', left: '50%', transform: 'translate(-50%,-50%)',
        width: '800px', height: '600px',
        background: 'radial-gradient(circle, rgba(0,255,136,0.08) 0%, transparent 65%)',
        zIndex: 0, pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 2, maxWidth: '900px' }}>
        {/* Live pill badge */}
        <motion.div
          initial={{ opacity: 0, y: -14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="font-grotesk"
          style={{
            display: 'inline-flex', alignItems: 'center', gap: '9px',
            padding: '6px 18px',
            background: 'rgba(0,255,136,0.08)',
            border: '1px solid rgba(0,255,136,0.28)',
            borderRadius: '100px',
            fontSize: '12px', color: '#c4c9e2', letterSpacing: '0.05em',
            marginBottom: '40px',
          }}
        >
          <span className="live-dot" />
          LIVE · manchester-homes.streamlit.app
        </motion.div>

        {/* Headline — word by word */}
        <motion.div
          variants={staggerWords}
          initial="hidden"
          animate="visible"
          className="font-syne headline-gradient"
          style={{
            fontSize: 'clamp(56px,9.5vw,96px)', fontWeight: 800,
            lineHeight: 1.0, letterSpacing: '-0.03em',
            display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.22em',
            marginBottom: '4px',
          }}
        >
          {['FIND', 'YOUR'].map(word => (
            <motion.span key={word} variants={wordVariant} style={{ display: 'inline-block' }}>{word}</motion.span>
          ))}
        </motion.div>
        <motion.div
          variants={staggerWords}
          initial="hidden"
          animate="visible"
          className="font-syne headline-gradient"
          style={{
            fontSize: 'clamp(56px,9.5vw,96px)', fontWeight: 800,
            lineHeight: 1.05, letterSpacing: '-0.03em',
            display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.22em',
            marginBottom: '32px',
          }}
        >
          <motion.span
            variants={{ hidden: { opacity: 0, y: 40 }, visible: { opacity: 1, y: 0, transition: { ...spring, delay: 0.2 } } }}
            style={{ display: 'inline-block' }}
          >
            PLACE.
          </motion.span>
        </motion.div>

        {/* Sub */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...spring, delay: 0.42 }}
          className="font-grotesk"
          style={{ fontSize: '18px', color: '#c4c9e2', maxWidth: '600px', margin: '0 auto 48px', lineHeight: 1.72, fontWeight: 400 }}
        >
          Live rental intelligence across Greater Manchester. Compare postcodes by affordability, yield, demand, and 6-month forecast trend.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...spring, delay: 0.6 }}
          style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '56px' }}
        >
          <motion.a
            href="https://manchester-homes.streamlit.app"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.04, boxShadow: '0 0 44px rgba(0,255,136,0.55)' }}
            whileTap={{ scale: 0.97 }}
            transition={spring}
            style={{
              padding: '15px 42px', background: '#00ff88', color: '#060810',
              fontFamily: 'Syne, sans-serif', fontSize: '14px', fontWeight: 700,
              letterSpacing: '0.1em', textDecoration: 'none', borderRadius: '8px', textTransform: 'uppercase',
            }}
          >
            Open Dashboard
          </motion.a>
          <motion.a
            href="https://github.com/privsmathewz"
            target="_blank"
            rel="noopener noreferrer"
            className="ghost-btn"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
            transition={spring}
            style={{
              padding: '15px 42px', background: 'transparent',
              border: '1px solid rgba(255,255,255,0.2)', color: 'rgba(255,255,255,0.7)',
              fontFamily: 'Syne, sans-serif', fontSize: '14px', fontWeight: 600,
              letterSpacing: '0.1em', textDecoration: 'none', borderRadius: '8px', textTransform: 'uppercase',
            }}
          >
            View on GitHub
          </motion.a>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2.2, ease: 'easeInOut' }}
          style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: '6px', color: 'rgba(0,255,136,0.45)' }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </motion.div>
      </div>
    </section>
  )
}

// ─── Market Pulse Strip ────────────────────────────────────────────────────
const PULSE_CARDS = [
  { label: 'BEST FOR STUDENTS', value: 'M14',      sub: 'Top-ranked student zone'  },
  { label: 'BEST YIELD',        value: '7.2%',     sub: 'Highest gross yield'       },
  { label: 'BEST VALUE',        value: '£850/mo',  sub: 'Lowest average rent'       },
  { label: 'MARKET TREND',      value: 'Rising',   sub: '+2.1% this quarter', up: true },
]

function PulseCard({ label, value, sub, up, delay }) {
  return (
    <motion.div
      className="pulse-card"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ ...spring, delay }}
      whileHover={{ y: -3, boxShadow: '0 0 32px rgba(0,255,136,0.18)' }}
    >
      <div className="pulse-shimmer" />
      <div className="font-grotesk" style={{ fontSize: '10px', fontWeight: 700, letterSpacing: '0.16em', color: '#00ff88', textTransform: 'uppercase', marginBottom: '8px' }}>{label}</div>
      <div className="font-syne"    style={{ fontSize: '24px', fontWeight: 800, color: up ? '#00ff88' : '#ffffff', marginBottom: '4px' }}>{value}</div>
      <div className="font-grotesk" style={{ fontSize: '11px', color: '#6b7280' }}>{sub}</div>
    </motion.div>
  )
}

function MarketPulse() {
  return (
    <section style={{ background: '#090c17', borderTop: '1px solid rgba(255,255,255,0.06)', borderBottom: '1px solid rgba(255,255,255,0.06)', padding: '52px 48px' }}>
      <div className="pulse-row" style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '20px' }}>
        {PULSE_CARDS.map((c, i) => <PulseCard key={c.label} {...c} delay={i * 0.08} />)}
      </div>
    </section>
  )
}

// ─── Product Showcase ──────────────────────────────────────────────────────
const SHOWCASE_BULLETS = [
  'Live choropleth map with yield and rent overlays by postcode',
  'ML-powered rent predictor trained on 10,000+ Manchester listings',
  'Persona-driven rankings for students, professionals, and investors',
]

function DashboardPreview() {
  const bars = [70, 85, 58, 95, 72]
  const tabs = ['Overview', 'Rankings', 'Live Map', 'Predictor', 'Trends']
  return (
    <div style={{ padding: '16px', height: '100%', display: 'flex', flexDirection: 'column', gap: '10px' }}>
      <div style={{ background: 'rgba(0,255,136,0.06)', border: '1px solid rgba(0,255,136,0.12)', borderRadius: '6px', padding: '9px 13px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span className="font-grotesk" style={{ fontSize: '9px', color: '#00ff88', fontWeight: 700, letterSpacing: '0.14em' }}>MANCHESTER RENTAL INTELLIGENCE</span>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', fontSize: '9px', color: '#6b7280', fontFamily: 'Space Grotesk' }}>
          <span style={{ width: '5px', height: '5px', background: '#00ff88', borderRadius: '50%', display: 'inline-block' }} /> LIVE
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '7px' }}>
        {[['£1,240', 'AVG RENT'], ['6.8%', 'AVG YIELD'], ['M14', 'TOP YIELD'], ['5', 'POSTCODES']].map(([v, l]) => (
          <div key={l} style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '6px', padding: '8px', textAlign: 'center' }}>
            <div className="font-syne" style={{ fontSize: '15px', fontWeight: 700, color: '#00ff88' }}>{v}</div>
            <div style={{ fontSize: '7px', color: '#6b7280', letterSpacing: '0.1em', fontFamily: 'Space Grotesk' }}>{l}</div>
          </div>
        ))}
      </div>

      <div style={{ background: 'rgba(255,255,255,0.02)', borderRadius: '7px', padding: '12px', flex: 1 }}>
        <div style={{ fontSize: '8px', color: '#6b7280', fontFamily: 'Space Grotesk', marginBottom: '9px', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Avg Rent by Postcode</div>
        <div style={{ display: 'flex', gap: '7px', alignItems: 'flex-end', height: '72px' }}>
          {bars.map((h, i) => (
            <div key={i} style={{ flex: 1, height: `${h}%`, background: `linear-gradient(to top, rgba(0,255,136,0.85), rgba(0,255,136,0.3))`, borderRadius: '3px 3px 0 0' }} />
          ))}
        </div>
        <div style={{ display: 'flex', gap: '7px', marginTop: '4px' }}>
          {['M1','M3','M5','M13','M14'].map(p => (
            <div key={p} style={{ flex: 1, textAlign: 'center', fontSize: '7px', color: '#4b5563', fontFamily: 'Space Grotesk' }}>{p}</div>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '5px' }}>
        {tabs.map(t => (
          <div key={t} style={{ flex: 1, background: t === 'Overview' ? 'rgba(0,255,136,0.1)' : 'rgba(255,255,255,0.03)', border: `1px solid ${t === 'Overview' ? 'rgba(0,255,136,0.35)' : 'rgba(255,255,255,0.05)'}`, borderRadius: '4px', padding: '5px 2px', textAlign: 'center', fontSize: '6.5px', color: t === 'Overview' ? '#00ff88' : '#6b7280', fontFamily: 'Space Grotesk', letterSpacing: '0.05em' }}>{t}</div>
        ))}
      </div>
    </div>
  )
}

function BrowserMockup({ scrollRef }) {
  const { scrollYProgress } = useScroll({ target: scrollRef, offset: ['start end', 'end start'] })
  const y = useTransform(scrollYProgress, [0, 1], [-18, 18])

  return (
    <motion.div className="browser-frame" style={{ y }}>
      <div className="browser-chrome">
        <div className="browser-dots">
          <span style={{ background: '#ff5f57' }} />
          <span style={{ background: '#febc2e' }} />
          <span style={{ background: '#28c840' }} />
        </div>
        <div className="browser-address">manchester-homes.streamlit.app</div>
      </div>
      <div className="browser-content">
        <DashboardPreview />
      </div>
    </motion.div>
  )
}

function ProductShowcase() {
  const ref = useRef(null)
  return (
    <section ref={ref} className="section-pad" style={{ padding: '110px 48px', background: '#060810' }}>
      <div className="product-grid" style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '80px', alignItems: 'center' }}>
        <div>
          <motion.div
            initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.5 }}
            className="font-grotesk"
            style={{ fontSize: '11px', letterSpacing: '0.22em', color: '#00ff88', textTransform: 'uppercase', marginBottom: '16px' }}
          >
            THE PLATFORM
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ ...spring, delay: 0.1 }}
            className="font-syne"
            style={{ fontSize: 'clamp(28px,4vw,48px)', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.02em', lineHeight: 1.1, marginBottom: '20px' }}
          >
            Every postcode.<br />Every metric.<br />One decision.
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ ...spring, delay: 0.2 }}
            className="font-grotesk"
            style={{ fontSize: '16px', color: 'rgba(255,255,255,0.48)', lineHeight: 1.78, marginBottom: '36px' }}
          >
            Manchester Homes aggregates live rental data across Greater Manchester, surfaces affordability signals, and makes them actionable — for students, professionals, and investors alike.
          </motion.p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {SHOWCASE_BULLETS.map((text, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ ...spring, delay: 0.3 + i * 0.1 }}
                style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00ff88" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: '2px' }}>
                  <polyline points="20 6 9 17 4 12" />
                </svg>
                <span className="font-grotesk" style={{ fontSize: '15px', color: 'rgba(255,255,255,0.68)', lineHeight: 1.6 }}>{text}</span>
              </motion.div>
            ))}
          </div>
        </div>

        <BrowserMockup scrollRef={ref} />
      </div>
    </section>
  )
}

// ─── Feature Grid ──────────────────────────────────────────────────────────
const FEATURES = [
  { icon: '🗺️', title: 'Live Map',       body: 'Choropleth map with real-time yield and rent overlays across all Manchester postcodes.' },
  { icon: '🏆', title: 'Rankings Engine', body: 'Side-by-side postcode rankings tailored to your persona — student, professional, or investor.' },
  { icon: '🤖', title: 'Rent Predictor',  body: 'Random Forest ML model delivers instant, data-driven rent estimates for any property type.' },
  { icon: '📈', title: 'Market Trends',   body: '6-month rolling trend charts showing rent trajectory and demand signals by area.' },
  { icon: '💰', title: 'Yield Analysis',  body: 'Gross yield calculator with property-type breakdown and market-average benchmarking.' },
  { icon: '👤', title: 'Persona Modes',   body: 'Switch between Student, Professional, Investor, and Explorer views instantly.' },
]

function FeatureGrid() {
  return (
    <section id="features" className="section-pad" style={{ padding: '110px 48px', background: '#090c17' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <motion.div
          initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.6 }}
          style={{ textAlign: 'center', marginBottom: '64px' }}
        >
          <h2 className="font-syne" style={{ fontSize: 'clamp(26px,4vw,44px)', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.02em', lineHeight: 1.2 }}>
            Built for people who make decisions<br />with data.
          </h2>
        </motion.div>

        <div className="feature-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '20px' }}>
          {FEATURES.map((card, i) => (
            <motion.div
              key={card.title}
              className="feat-card"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ ...spring, delay: i * 0.08 }}
              whileHover={{ y: -4, borderColor: 'rgba(0,255,136,0.5)', boxShadow: '0 0 32px rgba(0,255,136,0.14)' }}
              style={{ padding: '28px', background: 'rgba(13,13,26,0.95)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '14px', cursor: 'default' }}
            >
              <div style={{ fontSize: '30px', marginBottom: '16px', filter: 'drop-shadow(0 0 8px rgba(0,255,136,0.3))' }}>{card.icon}</div>
              <h3 className="font-syne"    style={{ fontSize: '18px', fontWeight: 700, color: '#ffffff', marginBottom: '10px' }}>{card.title}</h3>
              <p  className="font-grotesk" style={{ fontSize: '14px', color: 'rgba(255,255,255,0.43)', lineHeight: 1.72 }}>{card.body}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

// ─── Tech Stack Marquee ────────────────────────────────────────────────────
const TECHS = ['Python', 'Streamlit', 'Plotly', 'scikit-learn', 'React', 'Framer Motion', 'Netlify', 'Streamlit Cloud']

function TechStrip() {
  const doubled = [...TECHS, ...TECHS]
  return (
    <section style={{ background: '#060810', borderTop: '1px solid rgba(255,255,255,0.05)', borderBottom: '1px solid rgba(255,255,255,0.05)', padding: '32px 0' }}>
      <div style={{ textAlign: 'center', marginBottom: '22px' }}>
        <span className="font-grotesk" style={{ fontSize: '10px', letterSpacing: '0.24em', color: '#00ff88', textTransform: 'uppercase' }}>STACK</span>
      </div>
      <div className="marquee-wrapper">
        <div className="marquee-track">
          {doubled.map((t, i) => (
            <span key={i} className="marquee-pill">{t}</span>
          ))}
        </div>
      </div>
    </section>
  )
}

// ─── Final CTA ─────────────────────────────────────────────────────────────
function FinalCTA() {
  return (
    <section className="section-pad" style={{ padding: '130px 48px', background: 'radial-gradient(ellipse 80% 60% at 50% 50%, rgba(0,255,136,0.08) 0%, transparent 70%), #060810', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
      <motion.div
        initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ ...spring }}
      >
        <h2 className="font-syne" style={{ fontSize: 'clamp(34px,6vw,64px)', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.03em', marginBottom: '22px' }}>
          Ready to find your place?
        </h2>
        <p className="font-grotesk" style={{ fontSize: '18px', color: 'rgba(255,255,255,0.44)', marginBottom: '56px', maxWidth: '460px', margin: '0 auto 56px', lineHeight: 1.72 }}>
          Open the live dashboard and explore Manchester's rental market now.
        </p>

        <div style={{ position: 'relative', display: 'inline-block' }}>
          <motion.a
            href="https://manchester-homes.streamlit.app"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            transition={spring}
            style={{ display: 'inline-block', padding: '20px 64px', background: '#00ff88', color: '#060810', fontFamily: 'Syne, sans-serif', fontSize: '15px', fontWeight: 800, letterSpacing: '0.1em', textDecoration: 'none', borderRadius: '10px', textTransform: 'uppercase', position: 'relative', zIndex: 1 }}
          >
            Open Dashboard →
          </motion.a>
          {/* Pulsing ring */}
          <motion.div
            animate={{ scale: [1, 1.22, 1], opacity: [0.55, 0, 0.55] }}
            transition={{ repeat: Infinity, duration: 2.2, ease: 'easeInOut' }}
            style={{ position: 'absolute', inset: '-10px', border: '2px solid rgba(0,255,136,0.55)', borderRadius: '18px', pointerEvents: 'none', zIndex: 0 }}
          />
        </div>
      </motion.div>
    </section>
  )
}

// ─── Footer ────────────────────────────────────────────────────────────────
const FOOTER_LINKS = [
  ['Dashboard', 'https://manchester-homes.streamlit.app'],
  ['GitHub',    'https://github.com/privsmathewz'],
  ['LinkedIn',  'https://linkedin.com/in/sajanmathew'],
]

function Footer() {
  return (
    <footer style={{ background: '#060810', borderTop: '2px solid #00ff88', padding: '52px 48px 36px' }}>
      <div className="footer-grid" style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '40px', alignItems: 'start' }}>
        {/* Left */}
        <div>
          <div className="font-syne" style={{ fontSize: '17px', fontWeight: 800, color: '#00ff88', marginBottom: '12px', letterSpacing: '0.06em' }}>MANCHESTER HOMES</div>
          <div className="font-grotesk" style={{ fontSize: '13px', color: 'rgba(255,255,255,0.38)', lineHeight: 1.75 }}>
            Built by <span style={{ color: 'rgba(255,255,255,0.72)' }}>Sajan Mathew</span><br />
            MSc Data Science<br />
            Manchester Metropolitan University
          </div>
        </div>

        {/* Centre */}
        <div className="footer-center" style={{ textAlign: 'center' }}>
          <div className="font-grotesk" style={{ fontSize: '10px', letterSpacing: '0.2em', color: '#00ff88', textTransform: 'uppercase', marginBottom: '18px' }}>Navigation</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {FOOTER_LINKS.map(([label, href]) => (
              <motion.a
                key={label}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ color: '#00ff88' }}
                style={{ color: 'rgba(255,255,255,0.38)', textDecoration: 'none', fontFamily: 'Space Grotesk', fontSize: '14px', fontWeight: 500, transition: 'color 0.2s ease' }}
              >{label}</motion.a>
            ))}
          </div>
        </div>

        {/* Right */}
        <div className="footer-right" style={{ textAlign: 'right' }}>
          <div className="font-grotesk" style={{ fontSize: '10px', letterSpacing: '0.2em', color: '#00ff88', textTransform: 'uppercase', marginBottom: '18px' }}>Availability</div>
          <div className="font-grotesk" style={{ fontSize: '13px', color: 'rgba(255,255,255,0.38)', lineHeight: 1.8 }}>
            Graduate Route visa<br />
            No sponsorship required<br />
            <span style={{ color: '#00ff88', fontWeight: 600 }}>Available May 2026</span>
          </div>
        </div>
      </div>

      <div className="font-grotesk" style={{ maxWidth: '1200px', margin: '32px auto 0', paddingTop: '24px', borderTop: '1px solid rgba(255,255,255,0.05)', textAlign: 'center', fontSize: '11px', color: 'rgba(255,255,255,0.18)', letterSpacing: '0.07em' }}>
        © 2025 Manchester Homes · MSc Data Science Project · Manchester Metropolitan University
      </div>
    </footer>
  )
}

// ─── App ───────────────────────────────────────────────────────────────────
export default function App() {
  return (
    <AnimatePresence>
      <div style={{ minHeight: '100vh', background: '#060810' }}>
        <Navbar />
        <Hero />
        <MarketPulse />
        <ProductShowcase />
        <FeatureGrid />
        <TechStrip />
        <FinalCTA />
        <Footer />
      </div>
    </AnimatePresence>
  )
}

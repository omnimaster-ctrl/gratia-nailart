/* global React, ReactDOM, IOSFrame */
const { useState, useMemo } = React;

// ============ MOCK DATA ============
const today = new Date(2026, 4, 10); // May 10, 2026 (Sunday)
const weekDays = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
const monthNames = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];

const services = {
  acrilico: { name: 'Acrílico completo', dur: 180 },
  gel: { name: 'Gel completo', dur: 150 },
  pedi: { name: 'Pedicure spa', dur: 90 },
  rete: { name: 'Retoque', dur: 60 },
  naildesign: { name: 'Nail art personalizado', dur: 120 },
  semi: { name: 'Semipermanente', dur: 75 },
};

const bookings = [
  {
    id: 'b1', client: 'Sofía Ramírez', initials: 'SR', time: '09:00', day: 0,
    serviceKey: 'acrilico', extras: ['Diseño "Manantial Encantado"', 'Decoración con piedras'],
    phone: '+52 443 218 9034', status: 'confirmado', deposit: 200, depositPaid: true,
    notes: 'Prefiere forma almendra, largo medio. Alérgica a esmaltes con formaldehído.', visits: 7,
  },
  {
    id: 'b2', client: 'Valentina Cruz', initials: 'VC', time: '12:30', day: 0,
    serviceKey: 'gel', extras: ['Color "Ópalo Místico"'],
    phone: '+52 443 105 7821', status: 'pendiente', deposit: 150, depositPaid: false,
    notes: 'Primera cita. La encontró por Instagram.', visits: 1,
  },
  {
    id: 'b3', client: 'Daniela Ortega', initials: 'DO', time: '15:30', day: 0,
    serviceKey: 'rete', extras: [],
    phone: '+52 443 887 2210', status: 'confirmado', deposit: 100, depositPaid: true,
    notes: 'Retoque cada 3 semanas. Cliente recurrente.', visits: 14,
  },
  {
    id: 'b4', client: 'Renata Solís', initials: 'RS', time: '17:30', day: 0,
    serviceKey: 'naildesign', extras: ['Estilo "Espejo de Hada"'],
    phone: '+52 443 449 0173', status: 'pendiente', deposit: 250, depositPaid: false,
    notes: 'Quiere algo para su graduación. Trae referencia.', visits: 2,
  },
  // rest of week
  { id: 'b5', client: 'Camila Herrera', initials: 'CH', time: '10:00', day: 1, serviceKey: 'semi', extras: [], status: 'confirmado', deposit: 100, depositPaid: true, phone:'', notes:'', visits: 4 },
  { id: 'b6', client: 'Mariana Báez', initials: 'MB', time: '13:00', day: 1, serviceKey: 'pedi', extras: [], status: 'confirmado', deposit: 120, depositPaid: true, phone:'', notes:'', visits: 9 },
  { id: 'b7', client: 'Lucía Méndez', initials: 'LM', time: '11:00', day: 2, serviceKey: 'acrilico', extras: [], status: 'pendiente', deposit: 200, depositPaid: false, phone:'', notes:'', visits: 2 },
  { id: 'b8', client: 'Andrea Vega', initials: 'AV', time: '16:00', day: 2, serviceKey: 'gel', extras: [], status: 'confirmado', deposit: 150, depositPaid: true, phone:'', notes:'', visits: 5 },
  { id: 'b9', client: 'Paulina Aguilar', initials: 'PA', time: '09:30', day: 3, serviceKey: 'naildesign', extras: [], status: 'confirmado', deposit: 250, depositPaid: true, phone:'', notes:'', visits: 11 },
  { id: 'b10', client: 'Fernanda Ruiz', initials: 'FR', time: '14:00', day: 3, serviceKey: 'rete', extras: [], status: 'confirmado', deposit: 100, depositPaid: true, phone:'', notes:'', visits: 6 },
  { id: 'b11', client: 'Isabela Torres', initials: 'IT', time: '10:30', day: 4, serviceKey: 'acrilico', extras: [], status: 'pendiente', deposit: 200, depositPaid: false, phone:'', notes:'', visits: 1 },
  { id: 'b12', client: 'Carolina Pineda', initials: 'CP', time: '12:00', day: 5, serviceKey: 'semi', extras: [], status: 'confirmado', deposit: 100, depositPaid: true, phone:'', notes:'', visits: 8 },
  { id: 'b13', client: 'Ximena Lara', initials: 'XL', time: '15:00', day: 5, serviceKey: 'gel', extras: [], status: 'confirmado', deposit: 150, depositPaid: true, phone:'', notes:'', visits: 3 },
];

// ============ ATOMS ============
const StatusPill = ({ status, size = 'sm' }) => {
  const styles = {
    pendiente: { bg: 'rgba(205,162,85,0.18)', dot: '#cda255', fg: '#7a5d24' },
    confirmado: { bg: 'rgba(81,89,66,0.16)', dot: '#515942', fg: '#3d4435' },
    completado: { bg: 'rgba(138,141,126,0.22)', dot: '#8a8d7e', fg: '#5c6152' },
  }[status];
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      padding: size === 'lg' ? '6px 12px' : '4px 10px',
      borderRadius: 999, background: styles.bg, color: styles.fg,
      fontFamily: 'Manrope', fontSize: size === 'lg' ? 12 : 11,
      fontWeight: 600, letterSpacing: '0.5px', textTransform: 'uppercase',
    }}>
      <span style={{ width: 6, height: 6, borderRadius: 999, background: styles.dot }}></span>
      {status}
    </span>
  );
};

const ServiceAvatar = ({ initials, size = 44, tone = 'beige' }) => {
  const bg = tone === 'gold' ? '#cda255' : tone === 'olive' ? '#515942' : '#d6c9b0';
  const fg = tone === 'gold' ? '#fff' : tone === 'olive' ? '#e5e4d0' : '#3d4435';
  return (
    <div style={{
      width: size, height: size, borderRadius: 999, background: bg,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: 'Noto Serif', fontWeight: 700, fontSize: size * 0.36,
      color: fg, flexShrink: 0, letterSpacing: '-0.5px',
    }}>{initials}</div>
  );
};

const Icon = ({ name, size = 20, color = 'currentColor' }) => {
  const paths = {
    chevronLeft: 'M15 18l-6-6 6-6',
    chevronRight: 'M9 18l6-6-6-6',
    phone: 'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z',
    whatsapp: 'M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.4.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.7-.9-2.3-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4 0-.1-.2-.2-.5-.3z M12 2C6.5 2 2 6.5 2 12c0 1.7.5 3.4 1.3 4.8L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3C4.1 14.8 3.7 13.4 3.7 12 3.7 7.4 7.4 3.7 12 3.7s8.3 3.7 8.3 8.3-3.7 8-8.3 8z',
    clock: 'M12 6v6l4 2 M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10z',
    check: 'M5 12l5 5 10-11',
    checkCircle: 'M22 11.08V12a10 10 0 1 1-5.93-9.14 M22 4L12 14.01l-3-3',
    note: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8',
    cash: 'M2 7h20v10H2z M12 12c1.7 0 3-1.3 3-3s-1.3-3-3-3-3 1.3-3 3 1.3 3 3 3z M6 7v10 M18 7v10',
    home: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M9 22V12h6v10',
    calendar: 'M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z M16 2v4 M8 2v4 M3 10h18',
    user: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2 M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
    sparkle: 'M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5z M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8z',
    pin: 'M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z M12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
    plus: 'M12 5v14 M5 12h14',
    filter: 'M22 3H2l8 9.46V19l4 2v-8.54z',
    moreVert: 'M12 13a1 1 0 1 0 0-2 1 1 0 0 0 0 2z M12 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2z M12 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2z',
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      {paths[name].split(' M').map((p, i) => <path key={i} d={(i === 0 ? '' : 'M') + p} />)}
    </svg>
  );
};

// ============ TODAY VIEW ============
const TodayView = ({ onOpen }) => {
  const todays = bookings.filter(b => b.day === 0);
  const [filter, setFilter] = useState('todas');
  const filtered = filter === 'todas' ? todays : todays.filter(b => b.status === filter);
  const stats = {
    total: todays.length,
    confirmadas: todays.filter(b => b.status === 'confirmado').length,
    pendientes: todays.filter(b => b.status === 'pendiente').length,
    depositos: todays.filter(b => b.depositPaid).reduce((s, b) => s + b.deposit, 0),
  };

  return (
    <div style={{ paddingBottom: 140 }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(180deg, #515942 0%, #3d4435 100%)',
        padding: '60px 20px 28px', color: '#e5e4d0',
        borderRadius: '0 0 24px 24px',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 18 }}>
          <div>
            <div style={{ fontFamily: 'Manrope', fontSize: 12, fontWeight: 600, letterSpacing: '0.8px', textTransform: 'uppercase', color: '#cda255', marginBottom: 4 }}>
              Domingo · 10 de mayo
            </div>
            <h1 style={{
              fontFamily: 'Noto Serif', fontWeight: 400, fontSize: 32, lineHeight: 1.05,
              margin: 0, color: '#e5e4d0', letterSpacing: '-0.5px',
            }}>Hoy en el<br/><em style={{ color: '#cda255' }}>estudio</em></h1>
          </div>
          <div style={{
            width: 44, height: 44, borderRadius: 999,
            background: 'rgba(205,162,85,0.18)', border: '1.5px solid rgba(205,162,85,0.4)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 16, color: '#cda255',
          }}>H</div>
        </div>

        {/* Stat row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
          <StatTile label="Citas" value={stats.total} accent="cream" />
          <StatTile label="Confirmadas" value={stats.confirmadas} accent="cream" />
          <StatTile label="Pendientes" value={stats.pendientes} accent="gold" />
        </div>

        {/* Deposit summary */}
        <div style={{
          marginTop: 12, padding: '12px 14px',
          background: 'rgba(205,162,85,0.12)', borderRadius: 12,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
              <Icon name="sparkle" size={16} color="#cda255" />
              <span style={{ fontFamily: 'Manrope', fontSize: 11, fontWeight: 700, letterSpacing: '0.6px', textTransform: 'uppercase', color: '#cda255', whiteSpace: 'nowrap' }}>
                Anticipos recibidos
              </span>
            </div>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 22, color: '#cda255', lineHeight: 1, whiteSpace: 'nowrap' }}>
              ${stats.depositos}<span style={{ fontSize: 11, color: '#b7bba2', marginLeft: 4, fontFamily: 'Manrope', fontWeight: 600 }}>MXN</span>
            </div>
          </div>
          <div style={{ fontFamily: 'Manrope', fontSize: 11, color: '#b7bba2', marginTop: 6, paddingLeft: 24 }}>
            Solo visible para ti · {todays.filter(b => b.depositPaid).length} de {todays.length} citas
          </div>
        </div>
      </div>

      {/* Filter chips */}
      <div style={{ padding: '20px 20px 12px', display: 'flex', gap: 8, overflowX: 'auto', scrollbarWidth: 'none' }}>
        {[
          { k: 'todas', l: `Todas · ${stats.total}` },
          { k: 'pendiente', l: `Pendientes · ${stats.pendientes}` },
          { k: 'confirmado', l: `Confirmadas · ${stats.confirmadas}` },
        ].map(f => (
          <button key={f.k} onClick={() => setFilter(f.k)} style={{
            padding: '8px 16px', borderRadius: 999, border: 'none',
            background: filter === f.k ? '#cda255' : '#d6c9b0',
            color: filter === f.k ? '#fff' : '#5c6152',
            fontFamily: 'Manrope', fontSize: 13, fontWeight: 600,
            whiteSpace: 'nowrap', cursor: 'pointer', flexShrink: 0,
            letterSpacing: '0.2px',
          }}>{f.l}</button>
        ))}
      </div>

      {/* Booking list */}
      <div style={{ padding: '4px 20px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {filtered.map(b => (
          <BookingRow key={b.id} booking={b} onOpen={() => onOpen(b.id)} />
        ))}
        {filtered.length === 0 && (
          <div style={{ padding: 40, textAlign: 'center', fontFamily: 'Manrope', color: '#8a8d7e', fontSize: 14 }}>
            Sin citas en esta categoría.
          </div>
        )}
      </div>
    </div>
  );
};

const StatTile = ({ label, value, accent }) => (
  <div style={{
    background: accent === 'gold' ? 'rgba(205,162,85,0.18)' : 'rgba(229,228,208,0.08)',
    padding: '10px 12px', borderRadius: 12,
  }}>
    <div style={{
      fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 28,
      color: accent === 'gold' ? '#cda255' : '#e5e4d0', lineHeight: 1,
    }}>{value}</div>
    <div style={{
      fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, letterSpacing: '0.5px',
      textTransform: 'uppercase', color: '#b7bba2', marginTop: 4,
    }}>{label}</div>
  </div>
);

const BookingRow = ({ booking, onOpen }) => {
  const svc = services[booking.serviceKey];
  return (
    <div onClick={onOpen} style={{
      background: '#fff', borderRadius: 16, padding: '14px 14px 14px 0',
      boxShadow: '0 2px 8px rgba(42,46,37,0.06)',
      display: 'flex', alignItems: 'stretch', gap: 14, cursor: 'pointer',
      position: 'relative', overflow: 'hidden',
    }}>
      {/* time rail */}
      <div style={{
        width: 76, flexShrink: 0, background: '#e5e4d0',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        borderRadius: '16px 0 0 16px', padding: '8px 0',
      }}>
        <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 22, color: '#3d4435', letterSpacing: '-0.5px' }}>
          {booking.time}
        </div>
        <div style={{ fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, color: '#8a8d7e', marginTop: 2, letterSpacing: '0.4px' }}>
          {svc.dur} MIN
        </div>
      </div>

      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: 8, paddingRight: 4 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <ServiceAvatar initials={booking.initials} size={36} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 15, color: '#2a2e25', lineHeight: 1.2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {booking.client}
            </div>
            <div style={{ fontFamily: 'Manrope', fontSize: 12, color: '#5c6152', marginTop: 2 }}>
              {booking.visits === 1 ? 'Cliente nueva' : `${booking.visits}ª visita`}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, paddingLeft: 2 }}>
          <span style={{
            fontFamily: 'Manrope', fontSize: 13, color: '#3d4435', fontWeight: 500,
          }}>{svc.name}</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
          <StatusPill status={booking.status} />
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{
              fontFamily: 'Manrope', fontSize: 11, fontWeight: 600, color: booking.depositPaid ? '#3d4435' : '#cda255',
              letterSpacing: '0.3px',
            }}>
              {booking.depositPaid ? `✓ Anticipo $${booking.deposit}` : `Anticipo $${booking.deposit}`}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============ WEEK VIEW ============
const WeekView = ({ onOpen }) => {
  const [activeDay, setActiveDay] = useState(0);
  const dates = [10, 11, 12, 13, 14, 15, 16];
  // hour grid
  const hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18];

  return (
    <div style={{ paddingBottom: 140 }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(180deg, #515942 0%, #3d4435 100%)',
        padding: '60px 20px 18px', color: '#e5e4d0',
        borderRadius: '0 0 24px 24px',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
          <div>
            <div style={{ fontFamily: 'Manrope', fontSize: 12, fontWeight: 600, letterSpacing: '0.8px', textTransform: 'uppercase', color: '#cda255', marginBottom: 4 }}>
              Semana del 10 al 16
            </div>
            <h1 style={{ fontFamily: 'Noto Serif', fontWeight: 400, fontSize: 28, margin: 0, letterSpacing: '-0.3px' }}>
              Mayo <em style={{ color: '#cda255' }}>2026</em>
            </h1>
          </div>
          <div style={{ display: 'flex', gap: 6 }}>
            <button style={navBtn}><Icon name="chevronLeft" size={18} color="#e5e4d0" /></button>
            <button style={navBtn}><Icon name="chevronRight" size={18} color="#e5e4d0" /></button>
          </div>
        </div>

        {/* day strip */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', gap: 4 }}>
          {weekDays.map((d, i) => {
            const dayBookings = bookings.filter(b => b.day === i).length;
            const isActive = activeDay === i;
            const isToday = i === 0;
            return (
              <button key={i} onClick={() => setActiveDay(i)} style={{
                background: isActive ? '#cda255' : isToday ? 'rgba(205,162,85,0.15)' : 'transparent',
                border: 'none', borderRadius: 12, padding: '8px 0 10px', cursor: 'pointer',
                color: isActive ? '#fff' : '#e5e4d0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2,
              }}>
                <span style={{ fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, letterSpacing: '0.4px', textTransform: 'uppercase', opacity: isActive ? 1 : 0.7 }}>{d}</span>
                <span style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 18 }}>{dates[i]}</span>
                <span style={{
                  width: 6, height: 6, borderRadius: 999, marginTop: 2,
                  background: dayBookings === 0 ? 'transparent' : isActive ? '#fff' : '#cda255',
                }}></span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Day agenda */}
      <div style={{ padding: '18px 20px 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
          <div>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 20, color: '#2a2e25', letterSpacing: '-0.2px' }}>
              {['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'][activeDay]} {dates[activeDay]}
            </div>
            <div style={{ fontFamily: 'Manrope', fontSize: 13, color: '#5c6152', marginTop: 2 }}>
              {bookings.filter(b => b.day === activeDay).length} {bookings.filter(b => b.day === activeDay).length === 1 ? 'cita' : 'citas'} agendadas
            </div>
          </div>
          <button style={{
            width: 40, height: 40, borderRadius: 999, border: 'none',
            background: '#cda255', color: '#fff', cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 2px 8px rgba(205,162,85,0.4)',
          }}><Icon name="plus" size={20} color="#fff" /></button>
        </div>

        {/* Timeline */}
        <DayTimeline hours={hours} dayBookings={bookings.filter(b => b.day === activeDay)} onOpen={onOpen} />
      </div>
    </div>
  );
};

const navBtn = {
  width: 36, height: 36, borderRadius: 999,
  background: 'rgba(229,228,208,0.12)', border: 'none',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  cursor: 'pointer',
};

const DayTimeline = ({ hours, dayBookings, onOpen }) => {
  const HOUR_HEIGHT = 56;
  const startHour = hours[0];
  return (
    <div style={{
      position: 'relative', background: '#fff', borderRadius: 16, padding: '12px 0',
      boxShadow: '0 2px 8px rgba(42,46,37,0.06)', overflow: 'hidden',
    }}>
      {/* hour lines */}
      {hours.map((h, i) => (
        <div key={h} style={{
          height: HOUR_HEIGHT, display: 'flex', alignItems: 'flex-start',
          borderTop: i === 0 ? 'none' : '1px dashed rgba(138,141,126,0.25)',
          position: 'relative',
        }}>
          <div style={{
            width: 56, paddingLeft: 14, paddingTop: 4,
            fontFamily: 'Manrope', fontSize: 11, fontWeight: 600, color: '#8a8d7e', letterSpacing: '0.4px',
          }}>{h}:00</div>
        </div>
      ))}

      {/* booking blocks */}
      {dayBookings.map(b => {
        const [hh, mm] = b.time.split(':').map(Number);
        const top = 12 + ((hh - startHour) + mm / 60) * HOUR_HEIGHT;
        const height = (services[b.serviceKey].dur / 60) * HOUR_HEIGHT - 4;
        const isPending = b.status === 'pendiente';
        return (
          <div key={b.id} onClick={() => onOpen(b.id)} style={{
            position: 'absolute', left: 60, right: 14, top, height,
            background: isPending ? '#cda255' : '#515942',
            borderRadius: 10, padding: '8px 12px', cursor: 'pointer',
            color: isPending ? '#fff' : '#e5e4d0',
            boxShadow: isPending ? '0 2px 8px rgba(205,162,85,0.35)' : '0 2px 8px rgba(81,89,66,0.25)',
            display: 'flex', flexDirection: 'column', justifyContent: 'space-between', overflow: 'hidden',
          }}>
            <div>
              <div style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 13, lineHeight: 1.2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {b.client}
              </div>
              {height > 40 && (
                <div style={{ fontFamily: 'Manrope', fontSize: 11, opacity: 0.85, marginTop: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {services[b.serviceKey].name}
                </div>
              )}
            </div>
            <div style={{ fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, letterSpacing: '0.4px', textTransform: 'uppercase', opacity: 0.8 }}>
              {b.time} · {services[b.serviceKey].dur}min
            </div>
          </div>
        );
      })}
    </div>
  );
};

// ============ BOOKING DETAIL ============
const BookingDetail = ({ id, onBack }) => {
  const b = bookings.find(x => x.id === id) || bookings[0];
  const svc = services[b.serviceKey];
  const [completed, setCompleted] = useState(false);
  const [deposit, setDeposit] = useState(b.depositPaid);

  return (
    <div style={{ paddingBottom: 120 }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(180deg, #515942 0%, #3d4435 100%)',
        padding: '56px 16px 28px', color: '#e5e4d0',
        borderRadius: '0 0 24px 24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
          <button onClick={onBack} style={{
            display: 'flex', alignItems: 'center', gap: 4, background: 'transparent', border: 'none',
            color: '#cda255', fontFamily: 'Manrope', fontSize: 14, fontWeight: 600, cursor: 'pointer', padding: 4,
          }}>
            <Icon name="chevronLeft" size={20} color="#cda255" /> Hoy
          </button>
          <button style={navBtn}><Icon name="moreVert" size={18} color="#e5e4d0" /></button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <ServiceAvatar initials={b.initials} size={56} tone="gold" />
          <div style={{ flex: 1, minWidth: 0 }}>
            <h2 style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 24, margin: 0, color: '#e5e4d0', lineHeight: 1.15, letterSpacing: '-0.4px' }}>
              {b.client}
            </h2>
            <div style={{ fontFamily: 'Manrope', fontSize: 13, color: '#b7bba2', marginTop: 4 }}>
              {b.visits === 1 ? 'Cliente nueva' : `Cliente recurrente · ${b.visits} visitas`}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <ActionBtn icon="whatsapp" label="WhatsApp" />
          <ActionBtn icon="phone" label="Llamar" />
          <ActionBtn icon="pin" label="Ubicación" />
        </div>
      </div>

      <div style={{ padding: '20px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {/* Appointment card */}
        <DetailCard>
          <CardEyebrow>La cita</CardEyebrow>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, marginTop: 6 }}>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 30, color: '#2a2e25', letterSpacing: '-0.5px' }}>
              {b.time}
            </div>
            <div style={{ fontFamily: 'Manrope', fontSize: 14, color: '#5c6152' }}>
              Domingo 10 de mayo · {svc.dur} min
            </div>
          </div>
          <div style={{ marginTop: 14, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <StatusPill status={completed ? 'completado' : b.status} size="lg" />
            <span style={{ fontFamily: 'Manrope', fontSize: 13, color: '#5c6152' }}>
              Termina ~{addMinutes(b.time, svc.dur)}
            </span>
          </div>
        </DetailCard>

        {/* Services */}
        <DetailCard>
          <CardEyebrow>Servicio</CardEyebrow>
          <div style={{ marginTop: 10 }}>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 20, color: '#2a2e25', letterSpacing: '-0.2px' }}>
              {svc.name}
            </div>
            {b.extras.length > 0 && (
              <ul style={{ margin: '10px 0 0', padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 6 }}>
                {b.extras.map((e, i) => (
                  <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 8, fontFamily: 'Manrope', fontSize: 14, color: '#3d4435' }}>
                    <span style={{ width: 5, height: 5, borderRadius: 999, background: '#cda255', marginTop: 8, flexShrink: 0 }}></span>
                    {e}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </DetailCard>

        {/* Deposit card — gold-accented */}
        <div style={{
          background: deposit ? '#515942' : 'linear-gradient(135deg, #cda255 0%, #b8903d 100%)',
          borderRadius: 16, padding: '18px', color: '#fff',
          boxShadow: deposit ? '0 2px 8px rgba(81,89,66,0.2)' : '0 4px 16px rgba(205,162,85,0.35)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontFamily: 'Manrope', fontSize: 11, fontWeight: 700, letterSpacing: '0.8px', textTransform: 'uppercase', opacity: 0.85 }}>
                Anticipo
              </div>
              <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 36, marginTop: 4, letterSpacing: '-0.5px' }}>
                ${b.deposit}<span style={{ fontSize: 14, opacity: 0.7, marginLeft: 6 }}>MXN</span>
              </div>
              <div style={{ fontFamily: 'Manrope', fontSize: 13, marginTop: 6, opacity: 0.9 }}>
                {deposit ? 'Recibido vía transferencia' : 'Pendiente de recibir'}
              </div>
            </div>
            <button onClick={() => setDeposit(!deposit)} style={{
              padding: '8px 14px', borderRadius: 999, border: 'none',
              background: deposit ? '#cda255' : 'rgba(255,255,255,0.22)',
              color: '#fff', fontFamily: 'Manrope', fontSize: 12, fontWeight: 700,
              letterSpacing: '0.5px', textTransform: 'uppercase', cursor: 'pointer',
              backdropFilter: 'blur(8px)',
            }}>
              {deposit ? '✓ Cobrado' : 'Marcar'}
            </button>
          </div>
        </div>

        {/* Contact */}
        <DetailCard>
          <CardEyebrow>Contacto</CardEyebrow>
          <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
            <ContactRow icon="phone" label="Teléfono" value={b.phone || '+52 443 218 9034'} />
            <ContactRow icon="whatsapp" label="WhatsApp" value="Última conversación hace 2 días" />
          </div>
        </DetailCard>

        {/* Notes */}
        {b.notes && (
          <DetailCard>
            <CardEyebrow>Notas privadas</CardEyebrow>
            <p style={{
              margin: '10px 0 0', fontFamily: 'Manrope', fontSize: 14, color: '#3d4435',
              lineHeight: 1.55, fontStyle: 'italic',
            }}>"{b.notes}"</p>
          </DetailCard>
        )}
      </div>

      {/* Sticky complete button */}
      <div style={{
        position: 'absolute', bottom: 84, left: 16, right: 16,
        pointerEvents: 'none',
      }}>
        <button onClick={() => setCompleted(!completed)} style={{
          width: '100%', padding: '16px 20px', borderRadius: 14, border: 'none',
          background: completed ? '#515942' : '#cda255',
          color: '#fff', fontFamily: 'Manrope', fontSize: 15, fontWeight: 700,
          letterSpacing: '0.5px', textTransform: 'uppercase', cursor: 'pointer',
          boxShadow: '0 6px 20px rgba(205,162,85,0.45)', pointerEvents: 'auto',
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
        }}>
          {completed ? <><Icon name="check" size={18} color="#fff" /> Cita completada</> : 'Marcar como completada'}
        </button>
      </div>
    </div>
  );
};

const addMinutes = (time, mins) => {
  const [h, m] = time.split(':').map(Number);
  const total = h * 60 + m + mins;
  const nh = Math.floor(total / 60), nm = total % 60;
  return `${String(nh).padStart(2,'0')}:${String(nm).padStart(2,'0')}`;
};

const DetailCard = ({ children }) => (
  <div style={{
    background: '#fff', borderRadius: 16, padding: '16px 18px',
    boxShadow: '0 2px 8px rgba(42,46,37,0.06)',
  }}>{children}</div>
);
const CardEyebrow = ({ children }) => (
  <div style={{
    fontFamily: 'Manrope', fontSize: 11, fontWeight: 700, color: '#cda255',
    letterSpacing: '0.8px', textTransform: 'uppercase',
  }}>{children}</div>
);

const ActionBtn = ({ icon, label }) => (
  <button style={{
    flex: 1, padding: '10px 8px', borderRadius: 12,
    background: 'rgba(205,162,85,0.16)', border: '1px solid rgba(205,162,85,0.3)',
    color: '#cda255', cursor: 'pointer',
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
    fontFamily: 'Manrope', fontSize: 11, fontWeight: 600, letterSpacing: '0.4px',
  }}>
    <Icon name={icon} size={18} color="#cda255" />
    {label}
  </button>
);

const ContactRow = ({ icon, label, value }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
    <div style={{
      width: 36, height: 36, borderRadius: 999, background: '#e5e4d0',
      display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
    }}>
      <Icon name={icon} size={16} color="#515942" />
    </div>
    <div style={{ flex: 1 }}>
      <div style={{ fontFamily: 'Manrope', fontSize: 11, fontWeight: 600, color: '#8a8d7e', letterSpacing: '0.4px', textTransform: 'uppercase' }}>
        {label}
      </div>
      <div style={{ fontFamily: 'Manrope', fontSize: 14, color: '#2a2e25', marginTop: 2 }}>
        {value}
      </div>
    </div>
  </div>
);

// ============ BOTTOM NAV ============
const BottomNav = ({ active, onChange }) => {
  const tabs = [
    { k: 'today', l: 'Hoy', i: 'home' },
    { k: 'week', l: 'Semana', i: 'calendar' },
    { k: 'clients', l: 'Clientes', i: 'user' },
  ];
  return (
    <div style={{
      position: 'absolute', bottom: 0, left: 0, right: 0,
      background: 'rgba(245,243,228,0.98)', backdropFilter: 'blur(20px)',
      borderTop: '1px solid rgba(138,141,126,0.18)',
      padding: '10px 16px 34px',
      boxShadow: '0 -4px 16px rgba(42,46,37,0.08)',
      display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 4,
    }}>
      {tabs.map(t => {
        const isActive = active === t.k;
        return (
          <button key={t.k} onClick={() => onChange(t.k)} style={{
            background: 'transparent', border: 'none', cursor: 'pointer',
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
            padding: '6px 0', color: isActive ? '#cda255' : '#8a8d7e',
          }}>
            <Icon name={t.i} size={22} color={isActive ? '#cda255' : '#8a8d7e'} />
            <span style={{ fontFamily: 'Manrope', fontSize: 11, fontWeight: isActive ? 700 : 500, letterSpacing: '0.3px' }}>{t.l}</span>
          </button>
        );
      })}
    </div>
  );
};

// ============ CLIENT DIRECTORY ============
const clients = [
  { id: 'c1', name: 'Sofía Ramírez', initials: 'SR', visits: 7, last: 'Hace 3 semanas', next: 'Hoy 09:00', fav: 'Acrílico completo', loyalty: 'VIP', totalDeposits: 1400, phone: '+52 443 218 9034', joined: 'mar 2024', tags: ['Almendra', 'Largo medio'], notes: 'Alérgica a esmaltes con formaldehído. Prefiere diseños florales.' },
  { id: 'c2', name: 'Valentina Cruz', initials: 'VC', visits: 1, last: '—', next: 'Hoy 12:30', fav: 'Gel completo', loyalty: 'Nueva', totalDeposits: 0, phone: '+52 443 105 7821', joined: 'may 2026', tags: ['Primera cita'], notes: 'Llegó por Instagram. Pidió ver portafolio "Ópalo Místico".' },
  { id: 'c3', name: 'Daniela Ortega', initials: 'DO', visits: 14, last: 'Hace 3 semanas', next: 'Hoy 15:30', fav: 'Retoque', loyalty: 'VIP', totalDeposits: 1400, phone: '+52 443 887 2210', joined: 'sep 2023', tags: ['Recurrente', 'Cada 3 sem'], notes: 'Cliente más leal. Siempre puntual.' },
  { id: 'c4', name: 'Renata Solís', initials: 'RS', visits: 2, last: 'Hace 4 meses', next: 'Hoy 17:30', fav: 'Nail art personalizado', loyalty: 'Activa', totalDeposits: 250, phone: '+52 443 449 0173', joined: 'ene 2026', tags: ['Diseños complejos'], notes: '' },
  { id: 'c5', name: 'Camila Herrera', initials: 'CH', visits: 4, last: 'Hace 1 mes', next: 'Lun 10:00', fav: 'Semipermanente', loyalty: 'Activa', totalDeposits: 400, phone: '+52 443 552 1180', joined: 'oct 2025', tags: ['Tonos nude'], notes: '' },
  { id: 'c6', name: 'Mariana Báez', initials: 'MB', visits: 9, last: 'Hace 2 meses', next: 'Lun 13:00', fav: 'Pedicure spa', loyalty: 'VIP', totalDeposits: 1080, phone: '+52 443 712 3344', joined: 'jun 2024', tags: ['Pedicure'], notes: 'Recomienda mucho a sus amigas.' },
  { id: 'c7', name: 'Paulina Aguilar', initials: 'PA', visits: 11, last: 'Hace 1 mes', next: 'Jue 09:30', fav: 'Nail art personalizado', loyalty: 'VIP', totalDeposits: 2750, phone: '+52 443 220 5567', joined: 'feb 2024', tags: ['Diseños "Espejo de Hada"'], notes: 'Su set "Manantial Encantado" ganó el reposteo del mes.' },
  { id: 'c8', name: 'Andrea Vega', initials: 'AV', visits: 5, last: 'Hace 5 semanas', next: 'Mié 16:00', fav: 'Gel completo', loyalty: 'Activa', totalDeposits: 750, phone: '', joined: 'ago 2025', tags: ['Color clásico'], notes: '' },
  { id: 'c9', name: 'Isabela Torres', initials: 'IT', visits: 1, last: '—', next: 'Vie 10:30', fav: 'Acrílico completo', loyalty: 'Nueva', totalDeposits: 0, phone: '', joined: 'may 2026', tags: ['Primera cita'], notes: '' },
  { id: 'c10', name: 'Lucía Méndez', initials: 'LM', visits: 2, last: 'Hace 5 meses', next: 'Mié 11:00', fav: 'Acrílico completo', loyalty: 'Inactiva', totalDeposits: 300, phone: '', joined: 'dic 2025', tags: [], notes: 'No ha vuelto desde diciembre.' },
  { id: 'c11', name: 'Fernanda Ruiz', initials: 'FR', visits: 6, last: 'Hace 3 semanas', next: 'Jue 14:00', fav: 'Retoque', loyalty: 'VIP', totalDeposits: 600, phone: '', joined: 'jul 2024', tags: ['Recurrente'], notes: '' },
  { id: 'c12', name: 'Carolina Pineda', initials: 'CP', visits: 8, last: 'Hace 2 meses', next: 'Sáb 12:00', fav: 'Semipermanente', loyalty: 'VIP', totalDeposits: 800, phone: '', joined: 'mar 2024', tags: ['Tonos pastel'], notes: '' },
  { id: 'c13', name: 'Ximena Lara', initials: 'XL', visits: 3, last: 'Hace 6 semanas', next: 'Sáb 15:00', fav: 'Gel completo', loyalty: 'Activa', totalDeposits: 450, phone: '', joined: 'nov 2025', tags: [], notes: '' },
];

const loyaltyTone = {
  VIP: { bg: 'rgba(205,162,85,0.18)', fg: '#8a6628', dot: '#cda255' },
  Activa: { bg: 'rgba(81,89,66,0.14)', fg: '#3d4435', dot: '#515942' },
  Nueva: { bg: 'rgba(161,139,99,0.18)', fg: '#7a6238', dot: '#a18b63' },
  Inactiva: { bg: 'rgba(138,141,126,0.18)', fg: '#5c6152', dot: '#8a8d7e' },
};

// Same loyalty pills, recoloured for the dark olive header surface
const loyaltyToneDark = {
  VIP: { bg: 'rgba(205,162,85,0.22)', fg: '#cda255' },
  Activa: { bg: 'rgba(229,228,208,0.18)', fg: '#e5e4d0' },
  Nueva: { bg: 'rgba(205,162,85,0.16)', fg: '#e0c68a' },
  Inactiva: { bg: 'rgba(229,228,208,0.12)', fg: '#b7bba2' },
};

const ClientsView = ({ onOpen }) => {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('todas');

  const filtered = clients.filter(c => {
    if (filter !== 'todas' && c.loyalty !== filter) return false;
    if (query && !c.name.toLowerCase().includes(query.toLowerCase())) return false;
    return true;
  });

  // group by letter
  const groups = {};
  filtered.slice().sort((a, b) => a.name.localeCompare(b.name)).forEach(c => {
    const k = c.name[0];
    (groups[k] = groups[k] || []).push(c);
  });

  const vipCount = clients.filter(c => c.loyalty === 'VIP').length;
  const nuevasCount = clients.filter(c => c.loyalty === 'Nueva').length;

  return (
    <div style={{ paddingBottom: 140 }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(180deg, #515942 0%, #3d4435 100%)',
        padding: '60px 20px 24px', color: '#e5e4d0',
        borderRadius: '0 0 24px 24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 18 }}>
          <div>
            <div style={{ fontFamily: 'Manrope', fontSize: 12, fontWeight: 600, letterSpacing: '0.8px', textTransform: 'uppercase', color: '#cda255', marginBottom: 4 }}>
              {clients.length} clientes
            </div>
            <h1 style={{ fontFamily: 'Noto Serif', fontWeight: 400, fontSize: 30, lineHeight: 1.05, margin: 0, letterSpacing: '-0.4px' }}>
              Tu <em style={{ color: '#cda255' }}>jardín</em><br/>de clientes
            </h1>
          </div>
          <button style={{
            width: 40, height: 40, borderRadius: 999, border: 'none',
            background: '#cda255', color: '#fff', cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 2px 8px rgba(205,162,85,0.4)',
          }}><Icon name="plus" size={18} color="#fff" /></button>
        </div>

        {/* Search */}
        <div style={{
          background: 'rgba(229,228,208,0.12)', borderRadius: 12,
          padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#b7bba2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Buscar por nombre…"
            style={{
              flex: 1, background: 'transparent', border: 'none', outline: 'none',
              color: '#e5e4d0', fontFamily: 'Manrope', fontSize: 14, fontWeight: 500,
            }}
          />
          {query && (
            <button onClick={() => setQuery('')} style={{
              background: 'transparent', border: 'none', color: '#b7bba2', cursor: 'pointer',
              fontFamily: 'Manrope', fontSize: 12,
            }}>Limpiar</button>
          )}
        </div>

        {/* Mini stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 8, marginTop: 12 }}>
          <MiniStat label="Total" value={clients.length} accent="cream" />
          <MiniStat label="VIP" value={vipCount} accent="gold" />
          <MiniStat label="Nuevas" value={nuevasCount} accent="cream" />
        </div>
      </div>

      {/* Filter chips */}
      <div style={{ padding: '18px 20px 8px', display: 'flex', gap: 8, overflowX: 'auto', scrollbarWidth: 'none' }}>
        {['todas', 'VIP', 'Activa', 'Nueva', 'Inactiva'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding: '8px 16px', borderRadius: 999, border: 'none',
            background: filter === f ? '#cda255' : '#d6c9b0',
            color: filter === f ? '#fff' : '#5c6152',
            fontFamily: 'Manrope', fontSize: 13, fontWeight: 600,
            whiteSpace: 'nowrap', cursor: 'pointer', flexShrink: 0,
          }}>{f === 'todas' ? `Todas · ${filtered.length}` : f}</button>
        ))}
      </div>

      {/* Grouped list */}
      <div style={{ padding: '4px 20px' }}>
        {Object.keys(groups).sort().map(letter => (
          <div key={letter} style={{ marginTop: 16 }}>
            <div style={{
              fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 14, color: '#cda255',
              letterSpacing: '1px', marginBottom: 8, paddingLeft: 4,
            }}>
              {letter.toUpperCase()}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {groups[letter].map(c => (
                <ClientRow key={c.id} client={c} onOpen={() => onOpen(c.id)} />
              ))}
            </div>
          </div>
        ))}
        {filtered.length === 0 && (
          <div style={{ padding: 40, textAlign: 'center', fontFamily: 'Manrope', color: '#8a8d7e', fontSize: 14 }}>
            Sin resultados.
          </div>
        )}
      </div>
    </div>
  );
};

const MiniStat = ({ label, value, accent }) => (
  <div style={{
    background: accent === 'gold' ? 'rgba(205,162,85,0.18)' : 'rgba(229,228,208,0.08)',
    padding: '8px 12px', borderRadius: 10,
  }}>
    <div style={{
      fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 22,
      color: accent === 'gold' ? '#cda255' : '#e5e4d0', lineHeight: 1,
    }}>{value}</div>
    <div style={{
      fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, letterSpacing: '0.5px',
      textTransform: 'uppercase', color: '#b7bba2', marginTop: 4,
    }}>{label}</div>
  </div>
);

const ClientRow = ({ client, onOpen }) => {
  const tone = loyaltyTone[client.loyalty];
  const isVIP = client.loyalty === 'VIP';
  return (
    <div onClick={onOpen} style={{
      background: '#fff', borderRadius: 14, padding: '12px 14px',
      boxShadow: '0 2px 8px rgba(42,46,37,0.06)',
      display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer',
      borderLeft: isVIP ? '3px solid #cda255' : '3px solid transparent',
    }}>
      <ServiceAvatar initials={client.initials} size={44} tone={isVIP ? 'gold' : 'beige'} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
          <span style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 15, color: '#2a2e25', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {client.name}
          </span>
          {isVIP && <Icon name="sparkle" size={12} color="#cda255" />}
        </div>
        <div style={{ fontFamily: 'Manrope', fontSize: 12, color: '#5c6152', display: 'flex', alignItems: 'center', gap: 6 }}>
          <span>{client.visits} {client.visits === 1 ? 'visita' : 'visitas'}</span>
          <span style={{ width: 2, height: 2, borderRadius: 999, background: '#8a8d7e' }}></span>
          <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', flex: 1 }}>{client.fav}</span>
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 6, flexShrink: 0 }}>
        <span style={{
          padding: '3px 8px', borderRadius: 999,
          background: tone.bg, color: tone.fg,
          fontFamily: 'Manrope', fontSize: 10, fontWeight: 700,
          letterSpacing: '0.5px', textTransform: 'uppercase',
        }}>{client.loyalty}</span>
        <span style={{ fontFamily: 'Manrope', fontSize: 11, color: '#8a8d7e', whiteSpace: 'nowrap' }}>
          {client.next}
        </span>
      </div>
    </div>
  );
};

const ClientDetail = ({ id, onBack }) => {
  const c = clients.find(x => x.id === id) || clients[0];
  const tone = loyaltyToneDark[c.loyalty];
  const isVIP = c.loyalty === 'VIP';

  return (
    <div style={{ paddingBottom: 140 }}>
      <div style={{
        background: 'linear-gradient(180deg, #515942 0%, #3d4435 100%)',
        padding: '56px 16px 24px', color: '#e5e4d0',
        borderRadius: '0 0 24px 24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
          <button onClick={onBack} style={{
            display: 'flex', alignItems: 'center', gap: 4, background: 'transparent', border: 'none',
            color: '#cda255', fontFamily: 'Manrope', fontSize: 14, fontWeight: 600, cursor: 'pointer', padding: 4,
          }}>
            <Icon name="chevronLeft" size={20} color="#cda255" /> Clientes
          </button>
          <button style={navBtn}><Icon name="moreVert" size={18} color="#e5e4d0" /></button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <ServiceAvatar initials={c.initials} size={60} tone={isVIP ? 'gold' : 'beige'} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <h2 style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 24, margin: 0, color: '#e5e4d0', letterSpacing: '-0.3px' }}>
              {c.name}
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
              <span style={{
                padding: '3px 10px', borderRadius: 999, background: tone.bg, color: tone.fg,
                fontFamily: 'Manrope', fontSize: 10, fontWeight: 700, letterSpacing: '0.5px', textTransform: 'uppercase',
              }}>{c.loyalty}</span>
              <span style={{ fontFamily: 'Manrope', fontSize: 12, color: '#b7bba2' }}>
                Desde {c.joined}
              </span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <ActionBtn icon="whatsapp" label="WhatsApp" />
          <ActionBtn icon="phone" label="Llamar" />
          <ActionBtn icon="calendar" label="Agendar" />
        </div>
      </div>

      <div style={{ padding: '20px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {/* Stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 8 }}>
          <StatBlock value={c.visits} label="Visitas" />
          <StatBlock value={`$${c.totalDeposits}`} label="Anticipos" small />
          <StatBlock value={c.last === '—' ? '—' : c.last.replace('Hace ', '')} label="Última cita" small />
        </div>

        {/* Next */}
        <div style={{
          background: 'linear-gradient(135deg, #cda255 0%, #b8903d 100%)',
          borderRadius: 16, padding: '14px 18px', color: '#fff',
          boxShadow: '0 4px 16px rgba(205,162,85,0.35)',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        }}>
          <div>
            <div style={{ fontFamily: 'Manrope', fontSize: 11, fontWeight: 700, letterSpacing: '0.8px', textTransform: 'uppercase', opacity: 0.9 }}>
              Próxima cita
            </div>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 22, marginTop: 4, letterSpacing: '-0.3px' }}>
              {c.next}
            </div>
            <div style={{ fontFamily: 'Manrope', fontSize: 13, marginTop: 2, opacity: 0.92 }}>
              {c.fav}
            </div>
          </div>
          <Icon name="chevronRight" size={24} color="#fff" />
        </div>

        {/* Preferences */}
        <DetailCard>
          <CardEyebrow>Preferencias</CardEyebrow>
          <div style={{ marginTop: 10 }}>
            <div style={{ fontFamily: 'Manrope', fontSize: 13, color: '#5c6152', marginBottom: 4 }}>
              Servicio frecuente
            </div>
            <div style={{ fontFamily: 'Noto Serif', fontWeight: 700, fontSize: 18, color: '#2a2e25', letterSpacing: '-0.2px' }}>
              {c.fav}
            </div>
            {c.tags.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 10 }}>
                {c.tags.map(t => (
                  <span key={t} style={{
                    padding: '5px 10px', borderRadius: 999,
                    background: '#e5e4d0', color: '#3d4435',
                    fontFamily: 'Manrope', fontSize: 11, fontWeight: 600,
                  }}>{t}</span>
                ))}
              </div>
            )}
          </div>
        </DetailCard>

        {/* Contact */}
        <DetailCard>
          <CardEyebrow>Contacto</CardEyebrow>
          <div style={{ marginTop: 10 }}>
            <ContactRow icon="phone" label="Teléfono" value={c.phone || 'No registrado'} />
          </div>
        </DetailCard>

        {/* Notes */}
        {c.notes && (
          <DetailCard>
            <CardEyebrow>Notas privadas</CardEyebrow>
            <p style={{
              margin: '10px 0 0', fontFamily: 'Manrope', fontSize: 14, color: '#3d4435',
              lineHeight: 1.55, fontStyle: 'italic',
            }}>"{c.notes}"</p>
          </DetailCard>
        )}
      </div>
    </div>
  );
};

const StatBlock = ({ value, label, small }) => (
  <div style={{
    background: '#fff', borderRadius: 12, padding: '12px',
    boxShadow: '0 2px 8px rgba(42,46,37,0.06)',
  }}>
    <div style={{
      fontFamily: 'Noto Serif', fontWeight: 700, fontSize: small ? 16 : 24,
      color: '#2a2e25', lineHeight: 1.1, letterSpacing: '-0.3px',
    }}>{value}</div>
    <div style={{
      fontFamily: 'Manrope', fontSize: 10, fontWeight: 600, letterSpacing: '0.5px',
      textTransform: 'uppercase', color: '#8a8d7e', marginTop: 6,
    }}>{label}</div>
  </div>
);

const App = () => {
  const [tab, setTab] = useState('today');
  const [detailId, setDetailId] = useState(null);
  const [clientId, setClientId] = useState(null);

  let view;
  if (detailId) view = <BookingDetail id={detailId} onBack={() => setDetailId(null)} />;
  else if (clientId) view = <ClientDetail id={clientId} onBack={() => setClientId(null)} />;
  else if (tab === 'today') view = <TodayView onOpen={setDetailId} />;
  else if (tab === 'week') view = <WeekView onOpen={setDetailId} />;
  else view = <ClientsView onOpen={setClientId} />;

  const showNav = !detailId && !clientId;

  return (
    <div data-screen-label="Admin Dashboard" style={{
      width: '100%', height: '100%', background: '#e5e4d0',
      overflowY: 'auto', overflowX: 'hidden', position: 'relative',
      fontFamily: 'Manrope, sans-serif',
    }}>
      {view}
      {showNav && <BottomNav active={tab} onChange={setTab} />}
    </div>
  );
};

window.GratiaAdmin = App;

import { Link } from 'react-router-dom';

import type { SessionPayload } from '../types/auth';

type HomePageProps = {
  me: SessionPayload;
};

export default function HomePage({ me }: HomePageProps) {
  return (
    <section className="spa-card p-6 md:p-8">
      <h2 className="text-xl font-bold">Migration Entry Point</h2>
      <p className="mt-2 text-white/75">
        This route is the new React shell. Legacy Django templates still run in parallel while feature cutover is in
        progress.
      </p>
      <div className="mt-5 spa-grid md:grid-cols-2">
        <Link to="/account" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Account Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Session login/register and profile update in SPA.</p>
        </Link>
        <Link to="/cafe" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Cafe Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Menu, cart, checkout, and previous orders.</p>
        </Link>
        <Link to="/cowork" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Cowork Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Spaces list, pricing preview, booking, and my bookings.</p>
        </Link>
      </div>
      <div className="mt-6 text-sm text-white/70">
        Session: {me.authenticated ? `Signed in as ${me.user?.full_name || me.user?.phone_number}` : 'Anonymous'}
      </div>
    </section>
  );
}


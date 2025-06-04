
import React from 'react';
import { BRAND_INFO } from '../constants.tsx';

const AboutPage: React.FC = () => {
  return (
    <div className="space-y-12 bg-brand-surface p-6 sm:p-10 rounded-lg shadow-2xl">
      <header className="text-center">
        <h1 className="text-4xl sm:text-5xl font-serif font-bold text-brand-text mb-3">
          Our Story: The Essence of {BRAND_INFO.name}
        </h1>
        <p className="text-lg text-brand-primary">{BRAND_INFO.tagline}</p>
      </header>

      <section className="grid md:grid-cols-2 gap-8 items-center">
        <div className="aspect-w-4 aspect-h-3 rounded-lg overflow-hidden shadow-lg">
          <img src="https://picsum.photos/seed/brand-history/800/600" alt="ChronoCraft Workshop" className="object-cover w-full h-full" />
        </div>
        <div>
          <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">A Legacy of Precision</h2>
          <p className="text-brand-text-secondary leading-relaxed mb-4">
            Founded on the principles of innovation and unwavering quality, {BRAND_INFO.name} ({BRAND_INFO.chineseName}) emerged from a vision to create timepieces that are both works of art and feats of engineering. Our journey began with a small atelier, where passionate watchmakers dedicated themselves to mastering the intricate dance of gears and springs.
          </p>
          <p className="text-brand-text-secondary leading-relaxed">
            Today, {BRAND_INFO.name} stands as a beacon of modern Chinese horology, blending age-old traditions with contemporary aesthetics. We believe a watch is more than an instrument; it's a companion through life's moments, a symbol of personal achievement, and an heirloom for generations to come.
          </p>
        </div>
      </section>

      <section>
        <h2 className="text-3xl font-serif font-semibold text-brand-text mb-6 text-center">The Art of Craftsmanship</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">Meticulous Assembly</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              Each {BRAND_INFO.name} watch is assembled by hand by our skilled artisans. Hundreds of components, some no larger than a human hair, are carefully pieced together to create a symphony of precision.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">Finest Materials</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              From surgical-grade stainless steel and aerospace titanium to ethically sourced precious metals and sapphire crystals, we select only materials that meet our exacting standards for durability and beauty.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">Rigorous Testing</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              Before a watch earns the {BRAND_INFO.name} insignia, it undergoes a battery of tests for accuracy, water resistance, and resilience, ensuring it performs flawlessly in any condition.
            </p>
          </div>
        </div>
      </section>

      <section className="text-center">
        <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">Our Philosophy</h2>
        <p className="text-brand-text-secondary leading-relaxed max-w-2xl mx-auto">
          "We don't just make watches; we craft time. Our philosophy is rooted in the belief that true luxury lies in the meticulous attention to detail, the pursuit of perfection, and the creation of objects that inspire. We invite you to experience the world of {BRAND_INFO.name} and find a timepiece that resonates with your spirit."
        </p>
        <p className="mt-4 text-md font-medium text-brand-primary">- The {BRAND_INFO.name} Team</p>
      </section>
    </div>
  );
};

export default AboutPage;

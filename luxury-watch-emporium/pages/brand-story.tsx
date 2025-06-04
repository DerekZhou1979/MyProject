import React from 'react';
import { BRAND_INFO } from '../seagull-brand-config';

const AboutPage: React.FC = () => {
  return (
    <div className="space-y-12 bg-brand-surface p-6 sm:p-10 rounded-lg shadow-2xl">
      <header className="text-center">
        <h1 className="text-4xl sm:text-5xl font-serif font-bold text-brand-text mb-3">
          品牌故事：{BRAND_INFO.chineseName}的传承
        </h1>
        <p className="text-lg text-brand-primary">{BRAND_INFO.tagline}</p>
      </header>

      <section className="grid md:grid-cols-2 gap-8 items-center">
        <div className="aspect-w-4 aspect-h-3 rounded-lg overflow-hidden shadow-lg">
          <img src="/images/seagull_background_(watch)_main.jpg" alt="海鸥表制表工坊" className="object-cover w-full h-full" />
        </div>
        <div>
          <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">70年制表传承</h2>
          <p className="text-brand-text-secondary leading-relaxed mb-4">
            {BRAND_INFO.chineseName}始创于1955年，是中国制表行业的开创者和领先者。70年来，品牌始终致力于高品质机芯的研发制造与中国原创机械腕表的研发生产。从一个小小的制表工坊开始，我们的制表大师们专注于掌握齿轮与发条的精密配合。
          </p>
          <p className="text-brand-text-secondary leading-relaxed">
            如今，{BRAND_INFO.chineseName}已发展为集机芯和成品表于一身，研发、生产、组装、销售于一体的企业集团。我们在追求创新卓越的道路上永不停息，成为现代中国钟表制造业的典范。
          </p>
        </div>
      </section>

      <section>
        <h2 className="text-3xl font-serif font-semibold text-brand-text mb-6 text-center">制表工艺</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">超复杂功能</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              融合三问报时、万年历、陀飞轮等多种超复杂功能的腕表，代表着世界制表业最顶级的技术和工艺。{BRAND_INFO.chineseName}是中国唯一攻克此难题的腕表品牌。
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">传统手艺</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              国家非物质文化遗产"花丝"工艺起源于先秦，海鸥传承华夏瑰宝，将纯银细丝，直径0.02毫米，相当于头发丝粗细的银丝，镶嵌并层层叠加于表盘之上。
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-semibold text-brand-primary mb-2">机芯技术</h3>
            <p className="text-sm text-brand-text-secondary leading-relaxed">
              每一枚{BRAND_INFO.chineseName}腕表都经过严格的精度、防水性和耐久性测试，确保在任何条件下都能完美运行。我们的机芯技术代表了中国制表工艺的最高水平。
            </p>
          </div>
        </div>
      </section>

      <section className="grid md:grid-cols-2 gap-8 items-center">
        <div>
          <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">大师系列</h2>
          <p className="text-brand-text-secondary leading-relaxed mb-4">
            大师海鸥系列代表了{BRAND_INFO.chineseName}最高制表技艺的巅峰之作。「三足金乌」三问报时金雕动偶腕表、「斗转星移」中华年历陀飞轮、「曜翼」立体陀飞轮等作品，每一枚都是传世经典。
          </p>
          <p className="text-brand-text-secondary leading-relaxed">
            这些腕表不仅展现了精湛的制表技艺，更承载着中华文化的深厚底蕴，将传统工艺与现代创新完美融合。
          </p>
        </div>
        <div className="aspect-w-4 aspect-h-3 rounded-lg overflow-hidden shadow-lg">
          <img src="/images/seagull_product_tourbillon_skeleton_main_skeleton.jpg" alt="海鸥表大师系列" className="object-cover w-full h-full" />
        </div>
      </section>

      <section className="text-center">
        <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">品牌理念</h2>
        <p className="text-brand-text-secondary leading-relaxed max-w-2xl mx-auto">
          "我们不仅仅是制造腕表，我们更是在雕琢时间。我们的理念根植于对细节的一丝不苟，对完美的不懈追求，以及对能够启发灵感的艺术品的创造。我们诚邀您体验{BRAND_INFO.chineseName}的世界，寻找与您心灵产生共鸣的时计伴侣。"
        </p>
        <p className="mt-4 text-md font-medium text-brand-primary">- {BRAND_INFO.chineseName}团队</p>
      </section>
    </div>
  );
};

export default AboutPage;

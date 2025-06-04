import { Product, ProductCategory } from '../seagull-watch-types';

// 海鸥表产品数据 - 基于官方产品信息
const mockProducts: Product[] = [
  {
    id: 'seagull-001',
    name: '「三足金乌」三问报时金雕动偶腕表',
    brand: '海鸥表',
    price: 298000.00,
    imageUrl: '/images/seagull_product_tourbillon_skeleton_main_gold.jpg',
    galleryImages: [
        '/images/seagull_product_tourbillon_skeleton_main_gold_01.jpg',
        '/images/seagull_product_tourbillon_skeleton_main_gold_02.png',
        '/images/seagull_product_tourbillon_skeleton_main_gold_03.png',
        '/images/seagull_detail_tourbillon_skeleton_main_01.jpg',
    ],
    shortDescription: '三问报时、万年历、陀飞轮超复杂功能于一体',
    description: '「三足金乌」三问报时金雕动偶腕表融合三问报时、万年历、陀飞轮等多种超复杂功能，是中国唯一攻克此难题的腕表品牌。机芯集435个精细零件于一体，其复杂的机械逻辑关系，需经验丰富的制表大师数月制作及调教。',
    features: ['三问报时', '万年历', '陀飞轮', '金雕工艺', '435个精细零件'],
    category: ProductCategory.LUXURY,
    stock: 3,
    sku: 'SG-SJW-001',
  },
  {
    id: 'seagull-002',
    name: '1963长空版飞行腕表',
    brand: '海鸥表',
    price: 3980.00,
    imageUrl: '/images/seagull_product_1963pilot_main_02.png',
    galleryImages: [
        '/images/seagull_product_1963pilot_main.png',
        '/images/seagull_product_1963pilot_main_01.png',
        '/images/seagull_detail_1963pilot_main_01.png',
        '/images/seagull_product_1963pilot_main_jewels.jpg',
    ],
    shortDescription: '经典飞行员腕表，传承1963年设计精髓',
    description: '1963长空版飞行腕表延续了海鸥表经典飞行员腕表的设计理念，搭载ST19机芯，拥有精准的计时功能和经典的飞行员表盘设计。这款腕表是对中国航空事业发展历程的致敬。',
    features: ['ST19机芯', '计时功能', '飞行员设计', '蓝宝石表镜', '100米防水'],
    category: ProductCategory.SPORTS,
    stock: 50,
    sku: 'SG-1963-002',
  },
  {
    id: 'seagull-003',
    name: '「曜翼」立体陀飞轮',
    brand: '海鸥表',
    price: 58000.00,
    imageUrl: '/images/seagull_product_tourbillon_skeleton_main.png',
    galleryImages: [
        '/images/seagull_product_tourbillon_skeleton_main.jpg',
        '/images/seagull_product_tourbillon_skeleton_main_02.png',
        '/images/seagull_product_tourbillon_skeleton_main_03.png',
        '/images/seagull_detail_tourbillon_skeleton.jpg',
    ],
    shortDescription: '立体陀飞轮，机械艺术的完美呈现',
    description: '「曜翼」立体陀飞轮腕表展现了海鸥表在复杂机械制表方面的深厚功力。立体陀飞轮装置在表盘上翩翩起舞，如同机械艺术品般令人着迷。',
    features: ['立体陀飞轮', '镂空表盘', '自动上链', '蓝宝石表镜', '透视表底'],
    category: ProductCategory.LUXURY,
    stock: 15,
    sku: 'SG-YY-003',
  },
  {
    id: 'seagull-004',
    name: '千米深潜潜水表',
    brand: '海鸥表',
    price: 4500.00,
    imageUrl: '/images/seagull_product_dive_main.png',
    galleryImages: [
      '/images/seagull_product_dive_main_01.png',
      '/images/seagull_product_dive_main_dive.png',
      '/images/seagull_background_dive.jpg',
    ],
    shortDescription: '专业潜水腕表，防水深度达1000米',
    description: '千米深潜潜水表是海鸥表为专业潜水员打造的工具腕表。具备1000米防水深度，配备单向旋转表圈和夜光指针，确保在深海环境中的可读性和安全性。',
    features: ['1000米防水', '单向旋转表圈', '夜光指针', '螺旋表冠', '不锈钢表链'],
    category: ProductCategory.SPORTS,
    stock: 35,
    sku: 'SG-DIVE-004',
  },
   {
    id: 'seagull-005',
    name: '小金砖女士腕表',
    brand: '海鸥表',
    price: 8800.00,
    imageUrl: '/images/seagull_product_women_main_gold.png',
    galleryImages: [
        '/images/seagull_product_women_main_gold_01.png',
        '/images/seagull_product_women_main_gold_02.png',
        '/images/seagull_product_women_main_gold_03.png',
        '/images/seagull_product_women_main_gold_04.png',
    ],
    shortDescription: '精致女士腕表，时间有她系列经典之作',
    description: '小金砖女士腕表是海鸥表"时间有她"系列的代表作品。采用18K金表壳，镶嵌精选钻石，表盘设计优雅精致，是现代女性的完美时计伴侣。',
    features: ['18K金表壳', '钻石镶嵌', '瑞士石英机芯', '蓝宝石表镜', '真皮表带'],
    category: ProductCategory.LUXURY,
    stock: 25,
    sku: 'SG-JZ-005',
  },
  {
    id: 'seagull-006',
    name: '复古电视机械腕表',
    brand: '海鸥表',
    price: 2980.00,
    imageUrl: '/images/seagull_product_retrotv_main.png',
    galleryImages: [
        '/images/seagull_product_retrotv_main_01.png',
        '/images/seagull_product_retrotv_main_zuan.png',
        '/images/seagull_product_retrotv_main_glitch.png',
    ],
    shortDescription: '创意设计机械腕表，复古与现代的完美融合',
    description: '复古电视机械腕表是海鸥表创新设计的代表作品。独特的方形表壳设计灵感来源于复古电视机，搭载机械机芯，将怀旧情怀与现代制表工艺完美结合。',
    features: ['方形表壳', '机械机芯', '创意设计', '不锈钢表链', '防水功能'],
    category: ProductCategory.MINIMALIST,
    stock: 40,
    sku: 'SG-TV-006',
  }
];

// 海鸥表产品服务 - 提供产品数据访问接口
export const productService = {
  // 获取产品列表（可按分类筛选）
  getProducts: async (category?: ProductCategory): Promise<Product[]> => {
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    if (category) {
      return mockProducts.filter(p => p.category === category);
    }
    return mockProducts;
  },
  // 根据ID获取单个产品
  getProductById: async (id: string): Promise<Product | undefined> => {
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300));
    return mockProducts.find(p => p.id === id);
  },
  // 获取所有产品分类
  getProductCategories: async (): Promise<ProductCategory[]> => {
    await new Promise(resolve => setTimeout(resolve, 100));
    return Object.values(ProductCategory);
  }
};

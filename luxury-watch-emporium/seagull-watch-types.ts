// 产品信息接口定义
export interface Product {
  id: string;           // 产品唯一标识
  name: string;         // 产品名称
  brand: string;        // 品牌名称
  price: number;        // 价格（人民币）
  imageUrl: string;     // 主图片URL
  galleryImages?: string[];  // 产品图片集
  description: string;  // 详细描述
  shortDescription: string;  // 简短描述
  features: string[];   // 产品特色功能
  category: ProductCategory; // 产品分类
  stock: number;        // 库存数量
  sku: string;          // 产品编码
}

// 海鸥表产品分类枚举
export enum ProductCategory {
  LUXURY = "大师海鸥",      // 顶级复杂功能系列
  SPORTS = "飞行系列",      // 飞行员腕表系列
  CLASSIC = "海洋系列",     // 潜水运动腕表系列
  MINIMALIST = "潮酷品线"   // 现代创意设计系列
}

// 购物车商品项接口（扩展Product，添加数量字段）
export interface CartItem extends Product {
  quantity: number;         // 购买数量
}

// 用户评价接口
export interface Review {
  id: string;              // 评价ID
  author: string;          // 评价作者
  rating: number;          // 评分 (1-5星)
  comment: string;         // 评价内容
  date: string;            // 评价日期
}

// 品牌信息接口
export interface BrandInfo {
  name: string;            // 英文品牌名
  chineseName: string;     // 中文品牌名
  tagline: string;         // 品牌标语
  logoSvg: React.ReactNode; // 品牌Logo SVG图标
}

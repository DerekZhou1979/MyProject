
export interface Product {
  id: string;
  name: string;
  brand: string;
  price: number;
  imageUrl: string;
  galleryImages?: string[];
  description: string;
  shortDescription: string;
  features: string[];
  category: ProductCategory;
  stock: number;
  sku: string;
}

export enum ProductCategory {
  CLASSIC = "Classic Elegance",
  SPORTS = "Sport & Adventure",
  LUXURY = "Luxury Collection",
  MINIMALIST = "Modern Minimalist"
}

export interface CartItem extends Product {
  quantity: number;
}

export interface Review {
  id: string;
  author: string;
  rating: number; // 1-5
  comment: string;
  date: string;
}

export interface BrandInfo {
  name: string;
  chineseName: string;
  tagline: string;
  logoSvg: React.ReactNode;
}

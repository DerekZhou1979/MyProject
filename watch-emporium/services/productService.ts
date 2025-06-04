
import { Product, ProductCategory } from '../types';

const mockProducts: Product[] = [
  {
    id: 'chrono-001',
    name: 'Aetherion Tourbillon',
    brand: 'ChronoCraft',
    price: 12500.00,
    imageUrl: 'https://picsum.photos/seed/aetherion/600/600',
    galleryImages: [
        'https://picsum.photos/seed/aetherion-g1/800/800',
        'https://picsum.photos/seed/aetherion-g2/800/800',
        'https://picsum.photos/seed/aetherion-g3/800/800',
    ],
    shortDescription: 'Exquisite flying tourbillon with celestial dial.',
    description: 'The Aetherion Tourbillon is a masterpiece of horological art, featuring a mesmerizing flying tourbillon and a deep blue aventurine dial reminiscent of a starry night sky. Encased in polished platinum, its movement is a testament to ChronoCraft\'s dedication to precision and beauty.',
    features: ['Flying Tourbillon', 'Aventurine Dial', 'Platinum Case', 'Sapphire Crystal', '50m Water Resistance'],
    category: ProductCategory.LUXURY,
    stock: 5,
    sku: 'CC-AT-001PT',
  },
  {
    id: 'chrono-002',
    name: 'Navigator GMT Chronograph',
    brand: 'ChronoCraft',
    price: 3800.00,
    imageUrl: 'https://picsum.photos/seed/navigator/600/600',
    galleryImages: [
        'https://picsum.photos/seed/navigator-g1/800/800',
        'https://picsum.photos/seed/navigator-g2/800/800',
    ],
    shortDescription: 'Robust GMT chronograph for the modern explorer.',
    description: 'Built for adventure, the Navigator GMT Chronograph combines rugged durability with sophisticated functionality. Its stainless steel case houses an automatic movement with GMT complication and a 12-hour chronograph, perfect for globetrotters and thrill-seekers.',
    features: ['Automatic Chronograph', 'GMT Function', 'Stainless Steel Case', 'Ceramic Bezel', '100m Water Resistance'],
    category: ProductCategory.SPORTS,
    stock: 25,
    sku: 'CC-NGC-002SS',
  },
  {
    id: 'chrono-003',
    name: 'Elegance Classic Date',
    brand: 'ChronoCraft',
    price: 1950.00,
    imageUrl: 'https://picsum.photos/seed/elegance/600/600',
    shortDescription: 'Timeless design with a refined silver dial.',
    description: 'The Elegance Classic Date embodies understated sophistication. Its clean lines, sunburst silver dial, and slim rose gold case make it an ideal companion for formal occasions or everyday wear. A true classic that transcends fleeting trends.',
    features: ['Automatic Movement', 'Date Complication', 'Rose Gold PVD Case', 'Guilloché Dial', 'Leather Strap'],
    category: ProductCategory.CLASSIC,
    stock: 40,
    sku: 'CC-ECD-003RG',
  },
  {
    id: 'chrono-004',
    name: 'Urban Minimalist Auto',
    brand: 'ChronoCraft',
    price: 1500.00,
    imageUrl: 'https://picsum.photos/seed/urban/600/600',
    galleryImages: [
      'https://picsum.photos/seed/urban-g1/800/800',
      'https://picsum.photos/seed/urban-g2/800/800',
      'https://picsum.photos/seed/urban-g3/800/800',
      'https://picsum.photos/seed/urban-g4/800/800',
    ],
    shortDescription: 'Sleek and modern automatic for city life.',
    description: 'The Urban Minimalist Auto is designed for the contemporary individual. Its stark matte black dial, devoid of numerals, and brushed titanium case create a powerful statement of modern design. The reliable automatic movement ensures you\'re always on time, in style.',
    features: ['Automatic Movement', 'Titanium Case', 'Matte Black Dial', 'Sapphire Crystal', 'Minimalist Design'],
    category: ProductCategory.MINIMALIST,
    stock: 30,
    sku: 'CC-UMA-004TI',
  },
   {
    id: 'chrono-005',
    name: 'Odyssey Moonphase',
    brand: 'ChronoCraft',
    price: 4200.00,
    imageUrl: 'https://picsum.photos/seed/odyssey/600/600',
    shortDescription: 'Captivating moonphase complication with an intricate dial.',
    description: 'The Odyssey Moonphase invites you to gaze upon the heavens. Its beautifully executed moonphase display is set against a deep midnight blue dial, complemented by a polished stainless steel case. A poetic expression of time\'s passage.',
    features: ['Automatic Movement', 'Moonphase Complication', 'Stainless Steel Case', 'Exhibition Caseback', 'Alligator Leather Strap'],
    category: ProductCategory.CLASSIC,
    stock: 15,
    sku: 'CC-OMP-005SS',
  },
  {
    id: 'chrono-006',
    name: 'Apex Diver Pro 300M',
    brand: 'ChronoCraft',
    price: 2900.00,
    imageUrl: 'https://picsum.photos/seed/apex/600/600',
    shortDescription: 'Professional-grade dive watch, water-resistant to 300m.',
    description: 'Engineered for the depths, the Apex Diver Pro 300M is a robust and reliable tool watch. Featuring a unidirectional rotating bezel, luminous markers for low-light visibility, and a helium escape valve, it\'s ready for any underwater challenge.',
    features: ['Automatic Movement', '300m Water Resistance', 'Unidirectional Bezel', 'Helium Escape Valve', 'Stainless Steel Bracelet'],
    category: ProductCategory.SPORTS,
    stock: 20,
    sku: 'CC-ADP-006SS',
  }
];

export const productService = {
  getProducts: async (category?: ProductCategory): Promise<Product[]> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    if (category) {
      return mockProducts.filter(p => p.category === category);
    }
    return mockProducts;
  },
  getProductById: async (id: string): Promise<Product | undefined> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    return mockProducts.find(p => p.id === id);
  },
  getProductCategories: async (): Promise<ProductCategory[]> => {
    await new Promise(resolve => setTimeout(resolve, 100));
    return Object.values(ProductCategory);
  }
};

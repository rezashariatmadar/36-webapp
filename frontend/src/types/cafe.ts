export interface CafeMenuItem {
  id: number;
  name: string;
  description?: string;
  price: number;
  is_available?: boolean;
}

export interface CafeMenuCategory {
  id: number;
  name: string;
  items: CafeMenuItem[];
}

export interface CartItem {
  item_id: number;
  name: string;
  quantity: number;
  subtotal: number;
}

export interface CartPayload {
  items: CartItem[];
  total: number;
  cart_count: number;
}

export interface CafeOrder {
  id: number;
  status: string;
  is_paid?: boolean;
  total_price: number;
  customer?: {
    full_name?: string;
    phone_number?: string;
  } | null;
}

export interface CafeCustomer {
  id: number;
  full_name: string;
  phone_number: string;
}


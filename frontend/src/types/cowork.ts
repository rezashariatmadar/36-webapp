export interface CoworkSpace {
  id: number;
  name: string;
  status: string;
  zone: string;
}

export interface CoworkZone {
  code: string;
  label: string;
  spaces: CoworkSpace[];
}

export interface CoworkBookingPreview {
  price: number;
  end_time: string;
  end_time_jalali: string;
}

export interface CoworkBooking {
  id: number;
  space_name: string;
  start_time: string;
  end_time: string;
  price_charged: number;
}


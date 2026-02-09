export interface UserRoles {
  is_admin: boolean;
  is_barista: boolean;
  is_customer: boolean;
}

export interface SessionUser {
  id: number;
  phone_number: string;
  full_name: string;
  national_id: string | null;
  birth_date: string | null;
  roles: UserRoles;
}

export interface SessionPayload {
  authenticated: boolean;
  csrf_token?: string;
  login_url?: string;
  logout_url?: string;
  user: SessionUser | null;
}

export interface StaffUserRecord {
  id: number;
  phone_number: string;
  full_name: string;
  role: 'Admin' | 'Barista' | 'Customer' | 'Unassigned';
  is_active: boolean;
  is_staff: boolean;
}


from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import MAX_CART_ITEMS, MAX_PER_ITEM, get_cart as _get_cart, save_cart as _save_cart
from .models import CafeOrder, MenuCategory, MenuItem, OrderItem
from accounts.models import CustomUser


def _as_price(value):
    if value is None:
        return 0
    return int(value)


class PublicMenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_name",
            "image_url",
            "is_available",
        ]

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.image.url
        return request.build_absolute_uri(obj.image.url)


class PublicMenuCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ["id", "name", "order", "items"]

    def get_items(self, obj):
        request = self.context.get("request")
        items = obj.items.filter(is_available=True).order_by("name")
        return PublicMenuItemSerializer(items, many=True, context={"request": request}).data


class OrderItemReadSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "menu_item_name", "quantity", "unit_price", "subtotal"]

    def get_subtotal(self, obj):
        return _as_price(obj.get_subtotal())


class CafeOrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = CafeOrder
        fields = [
            "id",
            "status",
            "is_paid",
            "notes",
            "total_price",
            "created_at",
            "updated_at",
            "items",
        ]


class StaffOrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    customer = serializers.SerializerMethodField()

    class Meta:
        model = CafeOrder
        fields = [
            "id",
            "status",
            "is_paid",
            "notes",
            "total_price",
            "created_at",
            "updated_at",
            "customer",
            "items",
        ]

    def get_customer(self, obj):
        if not obj.user:
            return None
        return {
            "id": obj.user.id,
            "phone_number": obj.user.phone_number,
            "full_name": obj.user.full_name,
        }


class StaffMenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "is_available", "category", "category_name"]


class StaffMenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["id", "name", "order"]


class StaffCustomerLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "full_name", "is_active"]


class StaffOrAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        has_auth = super().has_permission(request, view)
        if not has_auth:
            return False
        user = request.user
        return bool(user.is_staff or user.groups.filter(name__in=["Barista", "Admin"]).exists())


def _build_cart_payload(request):
    cart = _get_cart(request)
    fetched_items = MenuItem.objects.filter(id__in=cart.keys(), is_available=True).select_related("category")
    items_by_id = {str(item.id): item for item in fetched_items}

    payload_items = []
    total = 0
    changed = False

    for item_id, raw_quantity in list(cart.items()):
        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            cart.pop(item_id, None)
            changed = True
            continue

        if quantity <= 0:
            cart.pop(item_id, None)
            changed = True
            continue

        if quantity > MAX_PER_ITEM:
            quantity = MAX_PER_ITEM
            cart[item_id] = quantity
            changed = True

        item = items_by_id.get(str(item_id))
        if not item:
            cart.pop(str(item_id), None)
            changed = True
            continue

        subtotal = item.price * quantity
        total += subtotal
        payload_items.append(
            {
                "item_id": item.id,
                "name": item.name,
                "description": item.description,
                "category_name": item.category.name,
                "price": _as_price(item.price),
                "quantity": quantity,
                "subtotal": _as_price(subtotal),
                "image_url": request.build_absolute_uri(item.image.url) if item.image else None,
            }
        )

    if changed:
        _save_cart(request, cart)

    cart_count = sum(int(v) for v in cart.values() if str(v).isdigit())
    return {
        "items": payload_items,
        "cart_count": cart_count,
        "total": _as_price(total),
        "max_cart_items": MAX_CART_ITEMS,
        "max_per_item": MAX_PER_ITEM,
    }


class CafeMenuAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = MenuCategory.objects.prefetch_related("items").all()
        serializer = PublicMenuCategorySerializer(categories, many=True, context={"request": request})
        return Response({"categories": serializer.data})


class CafeCartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(_build_cart_payload(request))


class CafeCartItemsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        menu_item_id = request.data.get("menu_item_id")
        delta = request.data.get("delta", 1)
        try:
            menu_item_id = int(menu_item_id)
            delta = int(delta)
        except (TypeError, ValueError):
            return Response({"detail": "menu_item_id and delta must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        if delta not in (-1, 1):
            return Response({"detail": "delta must be 1 or -1."}, status=status.HTTP_400_BAD_REQUEST)

        cart = _get_cart(request)
        item_id_str = str(menu_item_id)

        if delta == 1:
            item = get_object_or_404(MenuItem, id=menu_item_id)
            if not item.is_available:
                return Response({"detail": "Item is unavailable."}, status=status.HTTP_409_CONFLICT)

            current_total = sum(int(v) for v in cart.values() if str(v).isdigit())
            if current_total >= MAX_CART_ITEMS:
                return Response({"detail": "Cart limit reached."}, status=status.HTTP_400_BAD_REQUEST)

            current_quantity = int(cart.get(item_id_str, 0))
            cart[item_id_str] = min(current_quantity + 1, MAX_PER_ITEM)
        else:
            if item_id_str in cart:
                quantity = int(cart[item_id_str])
                if quantity <= 1:
                    cart.pop(item_id_str, None)
                else:
                    cart[item_id_str] = quantity - 1

        _save_cart(request, cart)
        return Response(_build_cart_payload(request))


class CafeCheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = _get_cart(request)
        if not cart:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        notes = request.data.get("notes", "")
        with transaction.atomic():
            order = CafeOrder.objects.create(user=request.user, notes=notes)
            item_ids = [int(k) for k in cart.keys() if str(k).isdigit()]
            menu_items = MenuItem.objects.in_bulk(item_ids)

            order_items = []
            total_price = 0
            for item_id_str, quantity in cart.items():
                if not str(item_id_str).isdigit():
                    continue
                try:
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    continue

                if quantity < 1 or quantity > MAX_PER_ITEM:
                    continue

                menu_item = menu_items.get(int(item_id_str))
                if not menu_item:
                    continue
                if not menu_item.is_available:
                    return Response(
                        {"detail": f"Item '{menu_item.name}' is unavailable."},
                        status=status.HTTP_409_CONFLICT,
                    )

                order_items.append(
                    OrderItem(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        unit_price=menu_item.price,
                    )
                )
                total_price += menu_item.price * quantity

            if not order_items:
                return Response({"detail": "No valid cart items found."}, status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.bulk_create(order_items)
            order.total_price = total_price
            order.save(update_fields=["total_price", "updated_at"])

        _save_cart(request, {})
        return Response(
            {
                "order_id": order.id,
                "status": order.status,
                "total_price": _as_price(order.total_price),
            },
            status=status.HTTP_201_CREATED,
        )


class CafeOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = CafeOrder.objects.filter(user=request.user).prefetch_related("items__menu_item")
        serializer = CafeOrderReadSerializer(orders, many=True)
        return Response({"orders": serializer.data})


class CafeReorderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            CafeOrder.objects.prefetch_related("items__menu_item"),
            id=order_id,
            user=request.user,
        )
        cart = {}
        for item in order.items.all():
            cart[str(item.menu_item_id)] = min(item.quantity, MAX_PER_ITEM)
        _save_cart(request, cart)
        return Response(_build_cart_payload(request))


class CafeStaffOrdersAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def get(self, request):
        orders = (
            CafeOrder.objects.exclude(status__in=[CafeOrder.Status.DELIVERED, CafeOrder.Status.CANCELLED])
            .select_related("user")
            .prefetch_related("items__menu_item")
            .order_by("created_at")
        )
        serializer = StaffOrderReadSerializer(orders, many=True)
        return Response({"orders": serializer.data})


class CafeStaffOrderStatusAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def post(self, request, order_id):
        new_status = request.data.get("status")
        if new_status not in CafeOrder.Status.values:
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = get_object_or_404(CafeOrder.objects.select_for_update(), id=order_id)
            order.status = new_status
            order.save(update_fields=["status", "updated_at"])
        return Response({"order_id": order.id, "status": order.status})


class CafeStaffOrderPaymentToggleAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def post(self, request, order_id):
        with transaction.atomic():
            order = get_object_or_404(CafeOrder.objects.select_for_update(), id=order_id)
            order.is_paid = not order.is_paid
            order.save(update_fields=["is_paid", "updated_at"])
        return Response({"order_id": order.id, "is_paid": order.is_paid})


class CafeStaffMenuItemsAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def get(self, request):
        items = MenuItem.objects.select_related("category").order_by("category__name", "name")
        serializer = StaffMenuItemSerializer(items, many=True)
        return Response({"items": serializer.data})

    def post(self, request):
        name = (request.data.get("name") or "").strip()
        description = (request.data.get("description") or "").strip()
        price = request.data.get("price")
        category_id = request.data.get("category_id")
        is_available = bool(request.data.get("is_available", True))

        if not name or price is None or category_id is None:
            return Response({"detail": "name, price, and category_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        category = get_object_or_404(MenuCategory, id=category_id)
        try:
            item = MenuItem.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                is_available=is_available,
            )
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StaffMenuItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CafeStaffMenuCategoriesAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def get(self, request):
        categories = MenuCategory.objects.order_by("order", "name")
        serializer = StaffMenuCategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})


class CafeStaffMenuItemAvailabilityAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def post(self, request, item_id):
        item = get_object_or_404(MenuItem, id=item_id)
        item.is_available = not item.is_available
        item.save(update_fields=["is_available", "updated_at"])
        return Response({"item_id": item.id, "is_available": item.is_available})


class CafeStaffCustomerLookupAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def get(self, request):
        query = (request.query_params.get("q") or "").strip()
        if not query:
            return Response({"customers": []})
        users = (
            CustomUser.objects.filter(groups__name="Customer")
            .filter(Q(phone_number__icontains=query) | Q(full_name__icontains=query))
            .distinct()[:10]
        )
        serializer = StaffCustomerLookupSerializer(users, many=True)
        return Response({"customers": serializer.data})


class CafeStaffManualOrdersAPIView(APIView):
    permission_classes = [StaffOrAdminPermission]

    def post(self, request):
        items = request.data.get("items") or []
        if not isinstance(items, list) or not items:
            return Response({"detail": "items must be a non-empty list."}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = (request.data.get("phone_number") or "").strip()
        notes = request.data.get("notes") or "Walk-in Guest"
        customer = None
        if phone_number:
            customer = CustomUser.objects.filter(phone_number=phone_number).first()

        with transaction.atomic():
            order = CafeOrder.objects.create(user=customer, notes=notes, is_paid=True)
            total_price = 0
            order_items = []
            for item in items:
                menu_item_id = item.get("menu_item_id")
                quantity = item.get("quantity", 1)
                try:
                    menu_item_id = int(menu_item_id)
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    continue
                if quantity < 1 or quantity > MAX_PER_ITEM:
                    continue

                menu_item = MenuItem.objects.filter(id=menu_item_id).first()
                if not menu_item:
                    continue
                order_items.append(
                    OrderItem(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        unit_price=menu_item.price,
                    )
                )
                total_price += menu_item.price * quantity

            if not order_items:
                return Response({"detail": "No valid items."}, status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.bulk_create(order_items)
            order.total_price = total_price
            order.save(update_fields=["total_price", "updated_at"])
        return Response({"order_id": order.id, "total_price": _as_price(order.total_price)}, status=status.HTTP_201_CREATED)

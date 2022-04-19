from django.db import models
from datetime import datetime

from django.db.models import Sum

DISH_CATEGORIES = [
    (1, 'Главное блюдо'),
    (2, 'Гарнир'),
    (3, 'Соус'),
    (4, 'Вспомогательные продукты'),
]

TREATMENT_KIND = [
    (1, 'Первичная обработка'),
    (2, 'Тепловая обработка'),
]


class DishCategory(models.Model):
    dish_category = models.CharField(max_length=100, verbose_name="Категория блюда")

    def __str__(self):
        return self.dish_category

    class Meta:
        ordering = ('dish_category',)
        verbose_name = 'Категория блюда'
        verbose_name_plural = 'Категории блюд'


class TreatmentKind(models.Model):
    treatment_kind = models.CharField(max_length=100, verbose_name="Вид обработки")

    def __str__(self):
        return self.treatment_kind

    class Meta:
        ordering = ('treatment_kind',)
        verbose_name = 'Вид обработки'
        verbose_name_plural = 'Виды обработки'


class DateRange(models.Model):
    date_from = models.DateField(verbose_name="Начало диапазона")
    date_till = models.DateField(verbose_name="Окончание диапазона")

    def __str__(self):
        return "{0} - {1}".format(str(self.date_from), str(self.date_till))

    class Meta:
        ordering = ('date_from',)
        verbose_name = 'Диапазон дат'
        verbose_name_plural = 'Диапазоны дат'


class ProductGroup(models.Model):
    group_name = models.CharField(max_length=255, verbose_name="Название группы")
    order = models.IntegerField(verbose_name="Порядковый номер (для вывода в меню)", default=0)
    norm_per_day = models.FloatField(verbose_name="Норма на одного человека в сутки (брутто, грамм)", blank=True,
                                     null=True)
    replacement_for = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Является заменой для",
                                        blank=True, null=True)
    in_count = models.IntegerField(verbose_name="Норма по замене на 100 г. основного продукта", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.replacement_for is None:
            self.replacement_for = self
            self.save()

    def __str__(self):
        return "{0} - {1} г.".format(self.group_name, self.norm_per_day)

    @property
    def get_full_title(self):
        if self.replacement_for != self:
            repl = " замена для " + str(self.replacement_for.group_name)
        else:
            repl = ""
        return "{0}{1}".format(self.group_name, repl)

    class Meta:
        ordering = ('group_name',)
        verbose_name = 'Группа продуктов'
        verbose_name_plural = 'Группы продуктов'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name="Название продукта")
    wastage = models.ManyToManyField(DateRange, verbose_name="Потери при обработке", through="WastageByDateRange")
    energy_value = models.FloatField(verbose_name="Энергетическая ценность (кКал), 100 г.", default=0)
    proteins = models.FloatField(verbose_name="Белки, 100 г.", default=0)
    fats = models.FloatField(verbose_name="Жиры, 100 г.", default=0)
    carbohydrates = models.FloatField(verbose_name="Углеводы, 100 г.", default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for treatment_kind in TreatmentKind.objects.all():
            for date_range in DateRange.objects.all():
                WastageByDateRange.objects.get_or_create(product=self, date_range=date_range,
                                                         treatment_kind=treatment_kind,
                                                         defaults={'percent': 0}, )

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ('product_name',)
        verbose_name = 'Продукт питания'
        verbose_name_plural = 'Продукты питания'


class WastageByDateRange(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    date_range = models.ForeignKey(DateRange, verbose_name="Диапазон дат", on_delete=models.CASCADE)
    treatment_kind = models.ForeignKey(TreatmentKind, verbose_name="Вид обработки", on_delete=models.CASCADE)
    percent = models.FloatField(verbose_name="Потеря, %", default=0)

    def __str__(self):
        return "{0} {1} {2} {3}".format(str(self.product), str(self.date_range), str(self.treatment_kind),
                                        str(self.percent))

    class Meta:
        ordering = ('product',)
        verbose_name = 'Потеря по диапазону дат'
        verbose_name_plural = 'Потери по диапазону дат'


class WastageByHeatTreatment(models.Model):
    energy_value_wastage = models.FloatField(verbose_name="Потеря энергетическая ценности, %", default=0)
    proteins_wastage = models.FloatField(verbose_name="Потеря белка, %", default=0)
    fats_wastage = models.FloatField(verbose_name="Потеря жиров, %", default=0)
    carbohydrates_wastage = models.FloatField(verbose_name="Потеря углеводов, %", default=0)

    def __str__(self):
        return "Потери при тепловой обработке"

    class Meta:
        ordering = ('id',)
        verbose_name = 'Потеря при тепловой обработке (энергетическая ценность, белки, жиры, углеводы)'
        verbose_name_plural = 'Потери при тепловой обработке (энергетическая ценность, белки, жиры, углеводы)'


class Map(models.Model):
    map_number = models.CharField(verbose_name="Номер технологической карты", max_length=100)
    map_name = models.CharField(verbose_name="Название технологической карты", max_length=255)
    description = models.TextField(verbose_name="Описание технологического процесса", blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name="Продукты", through='ProductsInMap')

    def __str__(self):
        return 'Карта № {0} - {1}'.format(self.map_number, self.map_name)

    # получение масс нетто по категориям блюд (гарнир, основное блюдо и т.д.)
    def get_net_weights_by_dish_category(self, menu_date=datetime.now().date()):
        today_month = menu_date.month
        net_weight_dict = {}

        for dish_category in DishCategory.objects.all():
            # получаем все продукты этой категории блюда (гарнир, основное блюдо, соус и т.д.)
            products_in_dish = self.productsinmap_set.filter(dish_category=dish_category)
            dish_net_weight = 0
            # проходим по всем продуктам в карте
            for product_in_map in products_in_dish:
                # получаем исходную массу брутто
                product_in_map_net_weight = product_in_map.product_count_gross
                # проходим по всем обработкам продукта
                for treatment in product_in_map.treatments.all():
                    # получаем коэффициент потери
                    wastage = WastageByDateRange.objects.filter(product=product_in_map.product,
                                                                treatment_kind=treatment,
                                                                date_range__date_from__month__lte=today_month,
                                                                date_range__date_till__month__gte=today_month).first()
                    wastage_percent = wastage.percent if wastage else 0
                    # отнимаем потери при данном виде обработки
                    product_in_map_net_weight = product_in_map_net_weight - (
                            product_in_map_net_weight / 100 * wastage_percent)
                # добавляем массу нетто к подсчету
                dish_net_weight += product_in_map_net_weight
            net_weight_dict[dish_category.id] = round(dish_net_weight, 2)
        full_net_weight = 0
        for k in net_weight_dict:
            full_net_weight += net_weight_dict[k]
        net_weight_dict['full_net_weight'] = full_net_weight
        return net_weight_dict

    def get_values(self, menu_date=datetime.now().date()):
        today_month = menu_date.month
        energy_sum = 0
        protein_sum = 0
        fats_sum = 0
        carbohydrates_sum = 0
        net_weight_after_first_treatment_sum = 0
        wastage_values = WastageByHeatTreatment.objects.all().first()
        values_dict = {}

        for product_in_map in self.productsinmap_set.all():
            # масса брутто продукта
            product_count_gross = product_in_map.product_count_gross
            # считаем массу после первичной обработки
            wastage = WastageByDateRange.objects.filter(product=product_in_map.product,
                                                        treatment_kind_id=1,
                                                        date_range__date_from__month__lte=today_month,
                                                        date_range__date_till__month__gte=today_month).first()
            wastage_percent = wastage.percent if wastage else 0
            product_in_map_net_weight = product_count_gross - (product_count_gross / 100 * wastage_percent)
            product_in_map_net_weight = 0 if product_in_map_net_weight < 0 else product_in_map_net_weight

            # Пересчитываем на полную массу продукта (т.к. хранится на 100 г. продукта)
            protein_value_product = product_in_map_net_weight * product_in_map.product.proteins / 100
            fats_value_product = product_in_map_net_weight / 100 * product_in_map.product.fats
            carbohydrates_value_product = product_in_map_net_weight / 100 * product_in_map.product.carbohydrates
            energy_value_product = product_in_map_net_weight / 100 * product_in_map.product.energy_value

            protein_sum += protein_value_product
            fats_sum += fats_value_product
            carbohydrates_sum += carbohydrates_value_product
            energy_sum += energy_value_product
            net_weight_after_first_treatment_sum += product_in_map_net_weight

        full_net_weight = self.get_net_weights_by_dish_category(menu_date)['full_net_weight']
        try:
            values_dict['energy'] = round(energy_sum * (100 - wastage_values.energy_value_wastage) / full_net_weight, 2)
            values_dict['energy_full'] = round(energy_sum, 2)
        except ZeroDivisionError:
            values_dict['energy'] = 0
            values_dict['energy_full'] = 0
        try:
            values_dict['protein'] = round(protein_sum * (100 - wastage_values.proteins_wastage) / full_net_weight, 2)
            values_dict['protein_full'] = round(protein_sum, 2)
        except ZeroDivisionError:
            values_dict['protein'] = 0
            values_dict['protein_full'] = 0
        try:
            values_dict['fats'] = round(fats_sum * (100 - wastage_values.fats_wastage) / full_net_weight, 2)
            values_dict['fats_full'] = round(fats_sum, 2)
        except ZeroDivisionError:
            values_dict['fats'] = 0
            values_dict['fats_full'] = 0
        try:
            values_dict['carbohydrates'] = round(
                carbohydrates_sum * (100 - wastage_values.carbohydrates_wastage) / full_net_weight, 2)
            values_dict['carbohydrates_full'] = round(
                carbohydrates_sum * (100 - wastage_values.carbohydrates_wastage) / full_net_weight, 2)
        except ZeroDivisionError:
            values_dict['carbohydrates'] = 0
            values_dict['carbohydrates_full'] = 0
        return values_dict

    # Подсчет суммы масс брутто в карте по группе продуктов (норме)
    def get_product_group_value(self, product_group):
        value = self.productsinmap_set.all().filter(group__replacement_for=product_group).aggregate(Sum('product_count_gross_normalize'))['product_count_gross_normalize__sum']
        return value if value else 0

    # Подсчет количества указанного продукта в карте
    def get_product_count(self, product):
        count = self.productsinmap_set.filter(product=product).aggregate(Sum('product_count_gross'))[
            'product_count_gross__sum']
        return count if count else 0

    class Meta:
        ordering = ('map_name',)
        verbose_name = 'Технологическая карта'
        verbose_name_plural = 'Технологические карты'


class ProductsInMap(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name="Технологическая карта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    group = models.ForeignKey(ProductGroup, on_delete=models.SET_NULL, verbose_name="Группа продуктов", blank=True,
                              null=True)
    product_count_gross = models.FloatField(verbose_name="Масса брутто продукта")
    product_count_gross_normalize = models.FloatField(verbose_name="Масса брутто продукта (нормализованная)",
                                                      blank=True, null=True)
    dish_category = models.ForeignKey(DishCategory, on_delete=models.CASCADE, verbose_name="Категория блюда")
    treatments = models.ManyToManyField(TreatmentKind, verbose_name="Обработки продукта", blank=True)

    def save(self, *args, **kwargs):
        if self.group:
            self.product_count_gross_normalize = self.product_count_gross * 100 / self.group.in_count
            super().save(*args, **kwargs)

    def __str__(self):
        return str(self.map) + ' ' + str(self.product)

    def get_gross_count_normalize(self):
        return self.product_count_gross * 100 / self.group.in_count

    # общая масса нетто
    def get_net_weight(self):
        today = datetime.now().date()
        today_month = today.month
        product_in_map_net_weight = self.product_count_gross
        # проходим по всем обработкам продукта
        for treatment in self.treatments.all():
            # получаем коэффициент потери
            wastage = WastageByDateRange.objects.filter(product=self.product,
                                                        treatment_kind=treatment,
                                                        date_range__date_from__month__lte=today_month,
                                                        date_range__date_till__month__gte=today_month).first()
            # если не указан, то принимаем равным 0
            wastage_percent = wastage.percent if wastage else 0
            # отнимаем потери при данном виде обработки
            product_in_map_net_weight = product_in_map_net_weight - (product_in_map_net_weight / 100 * wastage_percent)
        product_in_map_net_weight = 0 if product_in_map_net_weight < 0 else product_in_map_net_weight
        return round(product_in_map_net_weight, 2)

    # общая масса нетто в виде массива по видам обработки
    def get_net_weight_treatment_array(self, menu_date=datetime.now().date()):
        today_month = menu_date.month
        product_in_map_net_weight = self.product_count_gross
        # проходим по всем обработкам продукта
        result_dict = {}
        for treatment in self.treatments.all().order_by('id'):
            # получаем коэффициент потери
            wastage = WastageByDateRange.objects.filter(product=self.product,
                                                        treatment_kind=treatment,
                                                        date_range__date_from__month__lte=today_month,
                                                        date_range__date_till__month__gte=today_month).first()
            # если не указан, то принимаем равным 0
            wastage_percent = wastage.percent if wastage else 0
            # отнимаем потери при данном виде обработки
            product_in_map_net_weight = product_in_map_net_weight - (product_in_map_net_weight / 100 * wastage_percent)
            product_in_map_net_weight = 0 if product_in_map_net_weight < 0 else product_in_map_net_weight
            result_dict[treatment.id] = round(product_in_map_net_weight, 2)
        return result_dict

    @property
    def get_net_weight_property(self):
        return self.get_net_weight()

    # нужно удалить
    @property
    def get_net_weight_treatment_array_property(self):
        return self.get_net_weight_treatment_array()

    @property
    def get_gross_count_normalize_property(self):
        return self.get_gross_count_normalize()

    class Meta:
        ordering = ('map',)
        verbose_name = 'Продукт в технологической карте'
        verbose_name_plural = 'Продукты в технологической карте'


class MealTime(models.Model):
    meal_time = models.CharField(max_length=100, verbose_name="Прием пищи")

    def __str__(self):
        return str(self.meal_time)

    class Meta:
        ordering = ('meal_time',)
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'


class MenuDay(models.Model):
    menu_day_date = models.DateField(verbose_name="Дата меню", unique=True)
    technological_maps = models.ManyToManyField(Map, verbose_name="Технологические карты",
                                                through='MapsInMenuDay')

    def __str__(self):
        return str(self.menu_day_date)

    class Meta:
        ordering = ('menu_day_date',)
        verbose_name = 'День меню'
        verbose_name_plural = 'Дни меню'


class MapsInMenuDay(models.Model):
    menu_day = models.ForeignKey(MenuDay, on_delete=models.CASCADE, verbose_name="День в меню")
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name="Технологическая карта")
    meal_time = models.ForeignKey(MealTime, on_delete=models.CASCADE, verbose_name="Прием пищи")

    def __str__(self):
        return '{0} {1} {2}'.format(str(self.menu_day), str(self.map), str(self.meal_time))

    class Meta:
        ordering = ('menu_day',)
        verbose_name = 'Технологическая карта в меню'
        verbose_name_plural = 'Технологические карты в меню'

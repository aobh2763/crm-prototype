import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.timezone import is_aware, make_naive
import datetime


class ExportStrategy:
    def export(self, queryset, fields=None):
        raise NotImplementedError("Subclasses must implement this method.")


class CSVStrategy(ExportStrategy):
    short_description = "Export selected rows to CSV"

    def export(self, queryset, fields=None):
        if not fields:
            fields = [f.name for f in queryset.model._meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={queryset.model.__name__}.csv'

        writer = csv.writer(response)
        writer.writerow(fields)

        for obj in queryset:
            row = []
            for f in fields:
                attr = getattr(obj, f, '')
                if callable(attr):
                    attr = attr()
                row.append(attr)
            writer.writerow(row)

        return response


class ExcelStrategy(ExportStrategy):
    short_description = "Export selected rows to Excel"

    def export(self, queryset, fields=None):
        if not fields:
            fields = [f.name for f in queryset.model._meta.fields]

        wb = Workbook()
        ws = wb.active
        ws.title = queryset.model.__name__

        # Header row
        ws.append(fields)

        for obj in queryset:
            row = []
            for f in fields:
                attr = getattr(obj, f, '')
                if callable(attr):
                    attr = attr()
                
                if isinstance(attr, datetime.datetime) and is_aware(attr):
                    attr = make_naive(attr)
                row.append(attr)
            ws.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={queryset.model.__name__}.xlsx'

        wb.save(response)
        return response


class PDFStrategy(ExportStrategy):
    short_description = "Export selected rows to PDF"

    def export(self, queryset, fields=None):
        if not fields:
            fields = [f.name for f in queryset.model._meta.fields]

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={queryset.model.__name__}.pdf'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        y = height - 40
        c.setFont("Helvetica", 10)
        c.drawString(40, y, f"{queryset.model.__name__} Export")
        y -= 30

        # Header
        c.drawString(40, y, " | ".join(fields))
        y -= 20

        for obj in queryset:
            row = []
            for f in fields:
                attr = getattr(obj, f, '')
                if callable(attr):
                    attr = attr()
                row.append(str(attr))
            line = " | ".join(row)
            c.drawString(40, y, line)
            y -= 15

            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40

        c.save()
        return response



def export_with_strategy(strategy_class):
    strategy = strategy_class()
    def action_func(modeladmin, request, queryset):
        fields = getattr(modeladmin, 'list_display', None)
        return strategy.export(queryset, fields)
    
    action_func.short_description = strategy_class.short_description
    action_func.__name__ = f"export_{strategy_class.__name__}"
    return action_func
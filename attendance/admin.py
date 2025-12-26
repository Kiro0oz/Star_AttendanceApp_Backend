from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    
    # الحقول التي ستظهر في قائمة سجلات الحضور
    list_display = (
        'user_name',        # اسم العضو
        'committee_name',   # اسم اللجنة (مستمد من الجلسة)
        'session_name',     # اسم الجلسة
        'check_in_time',    # وقت التسجيل الفعلي
        'status',           # (Present / Late)
        'is_registered',    # هل تم التسجيل سابقاً؟ (نعم/لا)
    )
    
    # الحقول التي يمكن البحث بها
    search_fields = ('user__username', 'user__first_name', 'session__name')
    
    # حقول للفلترة
    list_filter = ('session__committee', 'status', 'session__name', 'check_in_time')
    
    # الترتيب الافتراضي
    ordering = ('-check_in_time',)

    
    # لعرض الاسم الكامل للعضو
    @admin.display(description='Member Name')
    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    
    # لعرض اسم الجلسة
    @admin.display(description='Session Name')
    def session_name(self, obj):
        return obj.session.name
    
    # لعرض اسم اللجنة
    @admin.display(description='Committee')
    def committee_name(self, obj):
        # يمكن استخدام get_committee_display() للحصول على الاسم القابل للقراءة
        return obj.session.get_committee_display()
    
    # لعرض حالة التسجيل (للتوضيح)
    @admin.display(boolean=True, description='Registered')
    def is_registered(self, obj):
        return True # دائماً True طالما السجل موجود
    
    # منع التعديل اليدوي بعد التسجيل (قراءة فقط)
    def has_change_permission(self, request, obj=None):
        # السماح بالتغيير فقط للـ Superusers إذا أردت
        return request.user.is_superuser
    
    # جعل الحقول للقراءة فقط لتجنب تعديل توقيتات الحضور يدوياً
    readonly_fields = ('user', 'session', 'check_in_time', 'status')
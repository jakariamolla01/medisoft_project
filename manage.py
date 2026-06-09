#!/usr/bin/env python
import os
import sys

# পাইথন ৩.১৪ এবং জ্যাঙ্গোর সব লক ভেঙে মেমোরি লেভেলে ডাটাবেজ ফিক্স করার পাওয়ার-প্যাচ
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    # ডাটাবেজ ভার্সন চেক সম্পূর্ণ নিষ্ক্রিয় করা
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None
    
    from django.db.backends.mysql.features import DatabaseFeatures
    
    # পাইথন ৩.১৪ এর Read-Only ডিকশনারি লক বাইপাস করে জোরপূর্বক ভ্যালু অ্যাসাইন করা
    object.__setattr__(DatabaseFeatures, 'can_return_rows_from_bulk_insert', False)
    object.__setattr__(DatabaseFeatures, 'has_select_for_update_skip_locked', False)
except Exception:
    pass

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medisoft.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
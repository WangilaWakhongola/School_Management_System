from rest_framework import serializers
from .models import Book, BookIssue


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = '__all__'


class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()
    fine_due = serializers.SerializerMethodField()

    class Meta:
        model = BookIssue
        fields = '__all__'
        read_only_fields = ['issued_by', 'issue_date', 'fine_amount']

    def get_book_title(self, obj):
        return obj.book.title

    def get_borrower_name(self, obj):
        return obj.borrower.get_full_name()

    def get_fine_due(self, obj):
        return obj.calculate_fine()

    def create(self, validated_data):
        book = validated_data['book']
        if not book.is_available:
            raise serializers.ValidationError("This book is not available for issue.")
        validated_data['issued_by'] = self.context['request'].user
        book.available_copies -= 1
        book.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle return
        if validated_data.get('status') == 'returned' and instance.status == 'issued':
            instance.book.available_copies += 1
            instance.book.save()
            instance.fine_amount = instance.calculate_fine()
        return super().update(instance, validated_data)

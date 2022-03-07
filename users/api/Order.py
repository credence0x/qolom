
"""
    Order APIs
"""

class OrderCreateAPIView(generics.CreateAPIView):
    """
    UserProfile creates order
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, IsEndUser]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Interface Design for Testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them**

   ```C#
   // Testable
   public sealed class OrderProcessor
   {
      private readonly IPaymentGateway _paymentGateway;

      public OrderProcessor(IPaymentGateway paymentGateway)
      {
         _paymentGateway = paymentGateway;
      }

      public PaymentResult ProcessOrder(Order order)
      {
         return _paymentGateway.Charge(order.TotalPrice);
      }
   }   
   ```

2. **Return results, don't produce side effects**

   ```C#
   // Hard to test
   public sealed class OrderProcessor
   {
      public PaymentResult ProcessOrder(Order order)
      {
         var paymentGateway = new StripePaymentGateway();

         return paymentGateway.Charge(order.TotalPrice);
      }
   }
   ```

3. **Small surface area**
   - Fewer methods = fewer tests needed
   - Fewer params = simpler test setup

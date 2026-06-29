# When to Mock

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```C#
// Easy to mock
public interface IPaymentClient
{
    PaymentResult Charge(decimal amount);
}

public static class PaymentProcessor
{
    public static PaymentResult ProcessPayment(
        Order order,
        IPaymentClient paymentClient)
    {
        return paymentClient.Charge(order.Total);
    }
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```C#
// GOOD: Each function is independently mockable
// GOOD: specific operations are easy to mock
public interface IStimulator
{
    void SetIntensity(double milliamps);

    void StartPulse(TimeSpan duration);

    void Stop();
}

// BAD: mocking requires conditional logic inside the mock
public interface IDeviceConnection
{
    DeviceResponse SendCommand(string command, object? payload = null);
}
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

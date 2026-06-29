# Good and Bad Tests

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```C#
// GOOD: Tests observable behavior
[Fact]
public async Task User_Can_Checkout_With_Valid_Cart()
{
    // Arrange
    var cart = ShoppingCart.Create();

    cart.Add(Product);

    var paymentMethod = new CreditCardPaymentMethod();

    // Act
    CheckoutResult result =
        await CheckoutService.CheckoutAsync(
            cart,
            paymentMethod);

    // Assert
    Assert.Equal(
        OrderStatus.Confirmed,
        result.Status);
}
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```C#
// BAD: Tests implementation details
[Fact]
public async Task Checkout_Should_Call_PaymentService_Process()
{
    // Arrange
    var paymentService = new Mock<IPaymentService>();

    var cart = ShoppingCart.Create();

    cart.Add(new Product(name: "Headphones", price: 100m));

    // Act
    await CheckoutService.CheckoutAsync(cart, paymentService.Object);

    // Assert
    paymentService.Verify(x => x.Process(cart.Total), Times.Once);
}
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

Direct database, file, or storage inspection is acceptable when the storage contract itself is under test, or when no public read path exists and the test documents that boundary. Prefer public APIs for behavior tests.

```C#
// BAD: Bypasses interface to verify implementation details
[Fact]
public async Task CreateUser_Should_Save_To_Database()
{
    // Act
    await UserService.CreateUserAsync(new CreateUserRequest("Alice"));

    // BAD:
    // Direct database inspection couples the test
    // to storage implementation details
    UserRow? row =
        await Database.QuerySingleAsync<UserRow>(
            """
            SELECT *
            FROM Users
            WHERE Name = @Name
            """,
            new { Name = "Alice" });

    // Assert
    Assert.NotNull(row);
}

// GOOD: Verifies behaviour through the public interface
[Fact]
public async Task CreateUser_Should_Make_User_Retrievable()
{
    // Act
    User createdUser = await UserService.CreateUserAsync(new CreateUserRequest("Alice"));
    User retrievedUser = await UserService.GetUserAsync(createdUser.Id);

    // Assert
    Assert.Equal("Alice", retrievedUser.Name);
}
```

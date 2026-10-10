export class Ledger {
  private balance = 0;
  deposit(amount: number): number {
    if (amount <= 0) throw new Error("Invalid deposit amount");
    this.balance += amount;
    return this.balance;
  }
  getBalance(): number {
    return this.balance;
  }
}

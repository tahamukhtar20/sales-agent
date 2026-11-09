"""What the user tells us: the product being sold, and the account it's being sold to."""

from dataclasses import dataclass, field

import validators


@dataclass
class AccountBrief:
    # The seller's side
    product_name: str
    product_category: str
    value_proposition: str
    competitor_urls: list[str] = field(default_factory=list)
    product_notes: str = ""  # text extracted from an optional product document
    # The account being sold to
    account_url: str = ""
    contact_role: str = ""  # the person or title the meeting is with

    def errors(self) -> list[str]:
        problems = []
        if not self.product_name:
            problems.append("Enter the name of the product you're selling.")
        if not self.product_category:
            problems.append("Enter a product category.")
        if not self.value_proposition:
            problems.append("Describe the value proposition.")
        if not self.account_url or not validators.url(self.account_url):
            problems.append("Enter a valid website URL for the account you're meeting.")
        if not self.contact_role:
            problems.append("Enter who you're meeting, by name or job title.")
        problems += [f"Not a valid competitor URL: {url}" for url in self.competitor_urls if not validators.url(url)]
        return problems

    def seller_summary(self) -> str:
        return (
            f"Product: {self.product_name}\n"
            f"Category: {self.product_category}\n"
            f"Value proposition: {self.value_proposition}"
        )

# Design

## Coverage by the connector

The plugin advises only at shipment creation, never at rating, so the advisory and the connector's booking guard run at the same stage.
For 109 or 112 from Sweden to Great Britain the connector takes one of two paths.
With `product_matches` at `enforce` or `warn` and a verified lookup that does not offer the product, it refuses the booking or warns, and the message names the separate agreement and cites manual v5.26 §5.14 p.63 or §5.3 p.18.
With the guard off, or a lookup that cannot verify the product, the booking reaches DHL, and DHL's 22005 and 22026 rejections are followed by a `separate_agreement_lane` warning naming the agreement.
A shipper holding the agreement books without either message; the advisory warned that shipper on every booking.

## Territory reading

The Isle of Man scenario of "DHL Freight Sweden territory codes are read as their parent country" was observed through the removed advisory.
It is observed instead through the invoice copy advisory, whose 650 kr fee applies only to Great Britain, as the Jersey scenario already is.

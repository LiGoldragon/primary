Secondary owns deployment and production tests under its generation and
rollback gates. It does not design; it takes what the primary ripened and
puts it into production, and it tests there. A prototype that has not
passed the primary does not enter this layer.

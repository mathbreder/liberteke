from django.db.models import Field, Lookup


@Field.register_lookup
class SearchLookup(Lookup):
    lookup_name = 'search'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        print(vars(lhs), vars(rhs), params)
        return '%s <> %s' % (lhs, rhs), params

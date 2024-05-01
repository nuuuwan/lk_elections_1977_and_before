from utils import Log

log = Log('Validatable')


class Validatable:
    def validate(self, context=None):
        context = context or {}
        return []

    def validate_and_log(self):
        errors = self.validate()
        if not errors:
            log.debug('No errors.')
        else:
            for i_error, error in enumerate(errors, start=1):
                log.error(f'{i_error}) {error}')
        return errors
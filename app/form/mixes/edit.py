from app.form.mixes.create import MixCreateForm
from app.models.banner_record import BannerRecord
from app.models.mix_record import MixRecord


class MixEditForm(MixCreateForm):
    def update_entity(self, mix: MixRecord):
        mix.title = self.title.data
        mix.system = self.system.data
        mix.region = self.region.data
        mix.release = self.release.data

        if self.banner.data:
            mix.banner = BannerRecord(blob=self.banner.data.read())
        return mix

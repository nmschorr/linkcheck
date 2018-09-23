

class ProdConfig(object):
    site = "empty"
    just_name = "empty"
    just_stat = "empty"
    donefile_path = "empty"
    donefile = "empty"
    file_path = "empty"

    def set_site(self, site):
        self.site = site
    def get_site(self):
        return self.site
    def set_just_name(self, just_name):
        self.just_name = just_name
    def get_just_name(self):
        return self.just_name
    def set_just_stat(self, just_stat):
        self.just_stat = just_stat
    def get_just_stat(self):
        return self.just_stat
    def set_donefile(self, donefile):
        self.donefile = donefile
    def get_donefile(self):
        return self.donefile
    def set_file_path(self, file_path):
        self.file_path = file_path
    def get_file_path(self):
        return self.file_path
    def set_donefile_path(self, donefile_path):
        self.donefile_path = donefile_path
    def get_donefile_path(self):
        return self.donefile_path

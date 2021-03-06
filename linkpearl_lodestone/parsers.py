import re
import requests
from django.utils.text import slugify
from bs4 import BeautifulSoup
from linkpearl_lodestone.models import Race, Server, GrandCompany, Job, Title, Minion, Mount, FreeCompany, Character, Level

class BaseParser(object):
    USER_AGENT = u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    
    model_class = None
    
    def import_(self, **kwargs):
        obj = self.model_class(**kwargs)
        return self.update(obj)
    
    def update(self, obj):
        url = obj.get_lodestone_url()
        html = self.fetch(url)
        soup = self.consume(html)
        return self.save(soup, obj)
    
    def fetch(self, url):
        r = requests.get(url, headers={ 'User-Agent': self.USER_AGENT })
        r.raise_for_status()
        return r.text
    
    def consume(self, html):
        return BeautifulSoup(html, "lxml")
    
    def save(self, soup, obj):
        raise NotImplemented

class CharacterParser(BaseParser):
    GC_RANK_REGEXES = [
        re.compile(r'(\w+) Private Third Class'),
        re.compile(r'(\w+) Private Second Class'),
        re.compile(r'(\w+) Private First Class'),
        re.compile(r'(\w+) Corporal'),
        re.compile(r'(\w+) Sergeant Third Class'),
        re.compile(r'(\w+) Sergeant Second Class'),
        re.compile(r'(\w+) Sergeant First Class'),
        re.compile(r'Chief (\w+) Sergeant'),
        re.compile(r'Second (\w+) Lieutenant'),
    ]
    
    model_class = Character
    
    def save(self, soup, obj):
        # Sanity check for broken character profiles
        if soup.find(class_='hp').string == '0':
            return None
        
        
        # General Information
        name_box = soup.find(class_='player_name_txt').find('h2')
        name_link = name_box.find('a')
        race_box = soup.find(class_='chara_profile_title')
        
        id_s = filter(None, name_link['href'].split('/'))[-1]
        name_s = name_link.string
        server_s = name_box.find('span').string[2:-1]
        race_s, clan_s, gender_s = race_box.string.split(' / ')
        
        obj.lodestone_id = int(id_s)
        obj.server = Server.cached.get_or_create(name=server_s, defaults={'slug': slugify(server_s)})[0]
        obj.first_name, obj.last_name = name_s.split(' ')
        
        title_e = name_box.find(class_='chara_title')
        if title_e:
            title_s = title_e.string
            obj.title = Title.objects.get_or_create(name=title_s)[0]
        else:
            obj.title = None
        
        obj.race = Race.cached.get_or_create(name=race_s, defaults={'slug': slugify(race_s), 'clan_1': clan_s})[0]
        obj.clan = 1 if clan_s == obj.race.clan_1 else 2
        if obj.clan == 2 and not obj.race.clan_2:
            obj.race.clan_2 = clan_s
            obj.race.save()
        obj.gender = Character.GENDER_M if gender_s == u'\u2642' else Character.GENDER_F
        
        
        
        # Key/Value boxes
        fc_present = False
        for row in soup.find_all(class_='chara_profile_box_info'):
            key = row.find(class_='txt').string
            value_box = row.find(class_='txt_name')
            
            if key == u"Grand Company":
                gc_name, gc_rank_name = value_box.string.split('/')
                
                gc_rank_match = None
                obj.gc_rank = 0
                for i, rank_re in enumerate(CharacterParser.GC_RANK_REGEXES):
                    gc_rank_match = rank_re.match(gc_rank_name)
                    if gc_rank_match:
                        obj.gc_rank = i + 1
                        break
                
                try:
                    obj.gc = GrandCompany.cached.get(name=gc_name)
                except GrandCompany.DoesNotExist:
                    slug = slugify(gc_name.split(' ')[-1])
                    short = gc_rank_match.group(1)
                    obj.gc = GrandCompany.cached.create(name=gc_name, slug=slug, short=short)
            
            elif key == u"Free Company":
                fc_present = True
                
                fc_link = value_box.find('a')
                fc_name = fc_link.string
                fc_id = filter(None, fc_link['href'].split('/'))[-1]
                
                obj.fc = FreeCompany.objects.get_or_create(lodestone_id=fc_id, defaults={'name': fc_name})[0]
        
        if not fc_present:
            obj.fc = None
        
        
        
        # Attributes
        p_attr_spans = soup.find(class_='param_list_attributes').find_all('span')
        for i, attr in enumerate(['str', 'dex', 'vit', 'int', 'mnd', 'pie']):
            obj.attrs[attr] = int(p_attr_spans[i].string)
        
        ATTR_KEYS = {
            "Accuracy": 'acc',
            "Critical Hit Rate": 'crit',
            "Determination": 'det',
            "Defense": 'def',
            "Parry": 'par',
            "Magic Defense": 'mdef',
            "Attack Power": 'atk',
            "Skill Speed": 'sks',
            "Attack Magic Potency": 'mpot',
            "Healing Magic Potency": 'hpot',
            "Spell Speed": 'sps',
        }
        for attr_list in soup.find_all(class_='param_list'):
            for row in attr_list.find_all('li'):
                children = list(row.children)
                attr = children[0].string
                value = int(children[-1].string)
                if attr in ATTR_KEYS:
                    obj.attrs[ATTR_KEYS[attr]] = value
        
        e_str_or_0 = lambda e: int(e.string or 0) if e else 0
        obj.attrs['hp'] = e_str_or_0(soup.find(class_='hp'))
        obj.attrs['mp'] = e_str_or_0(soup.find(class_='mp'))
        obj.attrs['cp'] = e_str_or_0(soup.find(class_='cp'))
        obj.attrs['gp'] = e_str_or_0(soup.find(class_='gp'))
        obj.attrs['tp'] = e_str_or_0(soup.find(class_='tp'))
        
        
        
        # Save the character once basic data is populated
        obj.save()
        
        
        
        # Minions and Mounts
        mount_box, minion_box = soup.find_all(class_='minion_box')
        
        existing_mount_names = [ m.name for m in obj.mounts.all() ]
        for link in mount_box.find_all('a'):
            name = link['title']
            if not name in existing_mount_names:
                mount = Mount.cached.get_or_create(name=name)[0]
                obj.mounts.add(mount)
        
        existing_minion_names = [ m.name for m in obj.minions.all() ]
        for link in minion_box.find_all('a'):
            name = link['title']
            if not name in existing_minion_names:
                minion = Minion.cached.get_or_create(name=name)[0]
                obj.minions.add(minion)
        
        
        
        # Classes and levels
        levels = { level.job_id: level for level in obj.levels.all() }
        for table in soup.find_all(class_='class_list'):
            cells = table.find_all('td')
            for i in xrange(len(cells) / 3):
                name_cell = cells[(i * 3) + 0]
                level_cell = cells[(i * 3) + 1]
                exp_cell = cells[(i * 3) + 2]
                
                name_strings = list(name_cell.stripped_strings)
                
                # Skip layout filler cells
                if not name_strings:
                    continue
                
                # Skip not-yet-unlocked jobs
                if level_cell.string == '-':
                    continue
                
                name = name_strings[-1]
                level = int(level_cell.string)
                exp_at, exp_of = [int(x) for x in exp_cell.string.split(' / ')]
                
                job = Job.cached.get_or_create(name=name)[0]
                if job.id in levels:
                    lvl = levels[job.id]
                    lvl.level = level
                    lvl.exp_at = exp_at
                    lvl.exp_of = exp_of
                    lvl.save()
                else:
                    lvl = Level.objects.create(character=obj, job=job, level=level, exp_at=exp_at, exp_of=exp_of)
        
        
        
        # Save it again for good measure (no-op if unchanged)
        obj.save()

        return obj

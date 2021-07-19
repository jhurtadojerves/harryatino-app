const initTagify = () => {
    var input = document.getElementById('filter_tagity');
    var tagify = new Tagify(input, {
        //pattern: /^.{0,20}$/, // Validate typed tag(s) by Regex. Here maximum chars length is defined as "20"
        delimiters: ", ", // add new tags when a comma or a space character is entered
        //maxTags: 6,
        blacklist: ["fuck", "shit", "pussy"],
        keepInvalidTags: true, // do not remove invalid tags (but keep them marked as invalid)
        //whitelist: ["temple", "stun", "detective", "sign", "passion", "routine", "deck", "discriminate", "relaxation", "fraud", "attractive", "soft", "forecast", "point", "thank", "stage", "eliminate", "effective", "flood", "passive", "skilled", "separation", "contact", "compromise", "reality", "district", "nationalist", "leg", "porter", "conviction", "worker", "vegetable", "commerce", "conception", "particle", "honor", "stick", "tail", "pumpkin", "core", "mouse", "egg", "population", "unique", "behavior", "onion", "disaster", "cute", "pipe", "sock", "dialect", "horse", "swear", "owner", "cope", "global", "improvement", "artist", "shed", "constant", "bond", "brink", "shower", "spot", "inject", "bowel", "homosexual", "trust", "exclude", "tough", "sickness", "prevalence", "sister", "resolution", "cattle", "cultural", "innocent", "burial", "bundle", "thaw", "respectable", "thirsty", "exposure", "team", "creed", "facade", "calendar", "filter", "utter", "dominate", "predator", "discover", "theorist", "hospitality", "damage", "woman", "rub", "crop", "unpleasant", "halt", "inch", "birthday", "lack", "throne", "maximum", "pause", "digress", "fossil", "policy", "instrument", "trunk", "frame", "measure", "hall", "support", "convenience", "house", "partnership", "inspector", "looting", "ranch", "asset", "rally", "explicit", "leak", "monarch", "ethics", "applied", "aviation", "dentist", "great", "ethnic", "sodium", "truth", "constellation", "lease", "guide", "break", "conclusion", "button", "recording", "horizon", "council", "paradox", "bride", "weigh", "like", "noble", "transition", "accumulation", "arrow", "stitch", "academy", "glimpse", "case", "researcher", "constitutional", "notion", "bathroom", "revolutionary", "soldier", "vehicle", "betray", "gear", "pan", "quarter", "embarrassment", "golf", "shark", "constitution", "club", "college", "duty", "eaux", "know", "collection", "burst", "fun", "animal", "expectation", "persist", "insure", "tick", "account", "initiative", "tourist", "member", "example", "plant", "river", "ratio", "view", "coast", "latest", "invite", "help", "falsify", "allocation", "degree", "feel", "resort", "means", "excuse", "injury", "pupil", "shaft", "allow", "ton", "tube", "dress", "speaker", "double", "theater", "opposed", "holiday", "screw", "cutting", "picture", "laborer", "conservation", "kneel", "miracle", "primary", "nomination", "characteristic", "referral", "carbon", "valley", "hot", "climb", "wrestle", "motorist", "update", "loot", "mosquito", "delivery", "eagle", "guideline", "hurt", "feedback", "finish", "traffic", "competence", "serve", "archive", "feeling", "hope", "seal", "ear", "oven", "vote", "ballot", "study", "negative", "declaration", "particular", "pattern", "suburb", "intervention", "brake", "frequency", "drink", "affair", "contemporary", "prince", "dry", "mole", "lazy", "undermine", "radio", "legislation", "circumstance", "bear", "left", "pony", "industry", "mastermind", "criticism", "sheep", "failure", "chain", "depressed", "launch", "script", "green", "weave", "please", "surprise", "doctor", "revive", "banquet", "belong", "correction", "door", "image", "integrity", "intermediate", "sense", "formal", "cane", "gloom", "toast", "pension", "exception", "prey", "random", "nose", "predict", "needle", "satisfaction", "establish", "fit", "vigorous", "urgency", "X-ray", "equinox", "variety", "proclaim", "conceive", "bulb", "vegetarian", "available", "stake", "publicity", "strikebreaker", "portrait", "sink", "frog", "ruin", "studio", "match", "electron", "captain", "channel", "navy", "set", "recommend", "appoint", "liberal", "missile", "sample", "result", "poor", "efflux", "glance", "timetable", "advertise", "personality", "aunt", "dog"],
        transformTag: transformTag,
        dropdown: {
            enabled: 3,
        }
    });
    function transformTag(tagData) {
        var states = [
            'success',
            'primary',
            'danger',
            'success',
            'warning',
            'dark',
            'primary',
            'info'];

        tagData.class = 'tagify__tag tagify__tag-light--' + states[KTUtil.getRandomInt(0, 7)];

        if (tagData.value.toLowerCase() == 'shit') {
            tagData.value = 's✲✲t'
        }
    }
    tagify.on('add', function(e) {
        console.log(e.detail)
    });

    tagify.on('invalid', function(e) {
        console.log(e, e.detail);
    });

    document.querySelectorAll(".filter-tag").forEach(el => {
        tag = el.dataset;
        tag.value = el.innerHTML
        tagify.addTags([tag])
    })
    return tagify
}

const initFilter = () => {
    const tagify = initTagify();
    const filterField = document.getElementById("id_filter_field");
    const filterForm = document.getElementById("filterForm");
    const filterSend = document.getElementById("filterSend");

    const renderFilterResults = data => {
        document.querySelectorAll(".filter-result-input").forEach(input => {
            input.closest(".form-group").classList.add("d-none")
            if (input.name == "choices") input.required = false;
            if (input.name == "choices" && !data[input.name].length && input.tagName == "INPUT") {
                input.closest(".form-group").classList.remove("d-none")
                input.required = true;
            }
            if (data[input.name].length && input.tagName == "SELECT") {
                try{
                    input.querySelectorAll("option").forEach(opt => {
                        opt.remove();
                    });
                    $(input).select2("destroy");
                } catch {}
                input.closest(".form-group").classList.remove("d-none")
                $(input).select2({
                    data: data[input.name]
                });
                input.required = true;
            }
        });
        filterForm.querySelector("button").disabled = false;
    }
    
    $(filterField).select2({placeholder: "Selecccione un campo"});
    $(filterField).on('change', async event => {
        const self = event.currentTarget;
        let url = self.dataset.url.replace("searchfield", self.value)
        if (url) {
            let response = await fetch(url)
            data = await response.json();
            renderFilterResults(data);
        }
    }); 

    filterForm.addEventListener("submit", event => {
        event.preventDefault();
        const field = document.getElementById("id_filter_field");
        const lookup = document.querySelector("[name=lookups]");
        const search = document.querySelector(".filter-result:not(.d-none) > [name=choices]");

        let searchLabel = search.tagName=="SELECT"?search.selectedOptions[0].label:search.value
        searchLabel = searchLabel.length>10?searchLabel.substring(0,10) + "...":searchLabel
        const value = field.selectedOptions[0].label + ": " + lookup.selectedOptions[0].label + " " + searchLabel
        
        tag = {
            "value": value,
            "field": field.value,
            "lookup": lookup.value,
            "search": search.value
        }
        tagify.addTags([tag]);
    });

    filterSend.addEventListener("click", async event => {
        let url = event.currentTarget.dataset.url;
        let params = new FormData();
        tagify.value.forEach(tag => {
            params.append(tag.field + "__" + tag.lookup, tag.search)
        });
        params.append(
            "csrfmiddlewaretoken",
            filterForm.querySelector("[name=csrfmiddlewaretoken]").value
        )
        let response = await fetch(url, {
            method: "POST",
            body: params,
        });
        let data = await response.json();
        window.location.href = window.location.pathname
    });

    /* filterSend.addEventListener("click", event => {
        let url = new URL(window.location.href)
        url.search = ""
        tagify.value.forEach(tag => {
            url.searchParams.append(
                tag.field + "__" + tag.lookup,
                tag.search
            )
        });
        window.location.search = url.search
    }); */
}

document.addEventListener("DOMContentLoaded", event => {
    initFilter();
});
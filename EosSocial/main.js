const Format = imports.format;
const Gettext = imports.gettext;

const Config = imports.config;
const Path = imports.path;
const SocialBar = imports.socialBar;

function setupEnvironment() {
    Gettext.bindtextdomain(Config.GETTEXT_PACKAGE, Path.LOCALE_DIR);
    Gettext.textdomain(Config.GETTEXT_PACKAGE);

    // initialize the global shortcuts for localization
    window._ = Gettext.gettext;
    window.C_ = Gettext.pgettext;
    window.ngettext = Gettext.ngettext;

    String.prototype.format = Format.format;
}

function start() {
    setupEnvironment();

    let socialBar = new SocialBar.SocialBar();
    return socialBar.run(ARGV);
}

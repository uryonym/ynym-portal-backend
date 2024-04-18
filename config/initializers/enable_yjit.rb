if defined? RubyVM::YJIT.enable
  Raisl.application.config.after_initialize do
    RubyVM::YJIT.enable
  end
end

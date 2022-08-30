class CreateTasks < ActiveRecord::Migration[7.0]
  def change
    create_table :tasks, id: :uuid do |t|
      t.string :title, null: false
      t.string :description
      t.date :dead_line
      t.boolean :is_complete, null: false, default: false

      t.timestamps
    end
  end
end

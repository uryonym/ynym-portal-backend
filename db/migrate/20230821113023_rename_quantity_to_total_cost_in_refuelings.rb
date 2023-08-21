class RenameQuantityToTotalCostInRefuelings < ActiveRecord::Migration[7.0]
  def change
    rename_column :refuelings, :quantity, :total_cost
  end
end
